from sqlalchemy import func

from db import db
from models.enums import TicketState
from models.ticket import TicketModel
from models.users import RequesterUserModel, AgentUserModel, ManagerUserModel
from services.sendgrid_mail import SendEmailService
from services.translator import TranslateService


def translate(text, translate_to):
    try:
        translator = TranslateService()
        return translator.translate(text, translate_to)
    except Exception as ex:
        raise Exception(f"Translate Service Not Available! {ex}")


def ticket_update(pk, new_text, old_text, status):
    resolution_text_for_update = f"{old_text} | {new_text}"
    TicketModel.query.filter_by(pk=pk).update(
        {"status": status, "resolution_text": resolution_text_for_update}
    )


def send_email_helper(ticket, update_text_translated, case):
    to_email = ticket.requester.email
    requester_full_name = f"{ticket.requester.first_name} {ticket.requester.last_name}"
    ticket_title = ticket.title
    ticket_id = ticket.pk
    if case == "pending":
        subject = f"Ticket Number: {ticket_id} with title: {ticket_title} has been update. Your input is required!"
        body = (
            f"Dear {requester_full_name} the status of your ticket {ticket_id} was changed to pending. "
            f"*** {update_text_translated} ***"
        )
    elif case == "resolved":
        subject = f"{ticket_id}: {ticket_title} has been resolved!"
        body = (
            f"Dear {requester_full_name} your ticket {ticket_id} was resolved: *** {update_text_translated} "
            f"***. Please close it!"
        )
    try:
        send_email_service = SendEmailService()
        response = send_email_service.send_email(to_email, subject, body)
        assert response == 202
    except Exception as ex:
        raise Exception(f"Send Email Service Not Available! {ex}")


class TicketManager:
    @staticmethod
    def get_all_tickets(user):
        if isinstance(user, RequesterUserModel):
            return TicketModel.query.filter_by(requester_id=user.pk).all()
        elif isinstance(user, AgentUserModel):
            return TicketModel.query.filter_by(agent_id=user.pk).all()
        elif isinstance(user, ManagerUserModel):
            return TicketModel.query.filter_by(manager_id=user.pk).all()
        return TicketModel.query.all()

    @staticmethod
    def get_one_ticket(pk):
        return TicketModel.query.filter_by(pk=pk).first()

    @staticmethod
    def create(data, requester):
        data["requester_id"] = requester.pk
        ticket = TicketModel(**data)
        db.session.add(ticket)
        db.session.flush()
        return ticket

    @staticmethod
    def delete(pk):
        TicketModel.query.filter_by(pk=pk).delete()

    @staticmethod
    def assign(pk, agent_id):
        TicketModel.query.filter_by(pk=pk).update(
            {"status": TicketState.open, "agent_id": agent_id}
        )

    @staticmethod
    def priority(pk, priority):
        TicketModel.query.filter_by(pk=pk).update({"priority": priority})

    @staticmethod
    def pending(pk, pending_text):
        ticket = TicketModel.query.filter_by(pk=pk).first()
        ticket_update(pk, pending_text, ticket.resolution_text, TicketState.pending)
        pending_text_translated = translate(
            pending_text, ticket.requester.preferred_language.name
        )
        send_email_helper(ticket, pending_text_translated, "pending")

    @staticmethod
    def resolve(pk, resolution_text):
        ticket = TicketModel.query.filter_by(pk=pk).first()
        ticket_update(pk, resolution_text, ticket.resolution_text, TicketState.resolved)
        resolved_text_translated = translate(
            resolution_text, ticket.requester.preferred_language.name
        )
        send_email_helper(ticket, resolved_text_translated, "resolved")

    @staticmethod
    def update_description(pk, description):
        ticket = TicketModel.query.filter_by(pk=pk).first()
        description = f"{ticket.description} | {description}"
        TicketModel.query.filter_by(pk=pk).update(
            {"status": TicketState.resolved, "description": description}
        )

    @staticmethod
    def close(pk):
        TicketModel.query.filter_by(pk=pk).update(
            {"status": TicketState.closed, "closed_on": func.now()}
        )
