from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from db import db
from models import (
    TicketPriority,
    TicketState,
    TicketModel,
    RequesterUserModel,
)
from services.sendgrid_mail import SendEmailService
from services.translator import TranslateService
from tests.factories import (
    RequesterUserFactory,
    AgentUserFactory,
    ManagerUserFactory,
    AdministratorUserFactory,
)
from tests.helpers import generate_headers

TICKET_DATA = {
    "title": "Huge problem",
    "description": "I have no idea what the problem is!!!",
}
TICKETS_CREATED = 15


class TestTicket(TestCase):
    url_create_ticket = "/ticket/create/"

    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_ticket(self):
        user = RequesterUserFactory()
        headers = generate_headers(user)
        headers["Content-Type"] = "application/json"
        data = TICKET_DATA
        return self.client.post(
            self.url_create_ticket,
            headers=headers,
            json=data,
        )

    def assign_ticket(self, ticket_pk):
        agent = AgentUserFactory()
        manager = ManagerUserFactory()
        headers = generate_headers(manager)
        url_assign_ticket = f"/ticket/assign/{ticket_pk}/{agent.pk}/"
        return {
            "response": self.client.put(
                url_assign_ticket,
                headers=headers,
            ),
            "agent": agent,
            "headers": headers,
        }

    def test_create_ticket(self):
        response = self.create_ticket()
        assert response.status_code == 201
        response = response.json
        response.pop("created_on")
        expected_resp = {
            "title": TICKET_DATA["title"],
            "description": TICKET_DATA["description"],
            "pk": response["pk"],
            "priority": TicketPriority.low.name,
            "status": TicketState.new.name,
        }
        self.assertEqual(response, expected_resp)

    def test_assign_ticket(self):
        ticket_pk = self.create_ticket().json["pk"]
        result = self.assign_ticket(ticket_pk)
        assert result["response"].json == 204
        actual_agent_id = TicketModel.query.filter_by(pk=ticket_pk).first().agent_id
        self.assertEqual(actual_agent_id, result["agent"].pk)

    def test_update_ticket_priority(self):
        ticket_pk = self.create_ticket().json["pk"]
        result = self.assign_ticket(ticket_pk)
        priority = TicketPriority.high.name
        url_update_ticket_priority = f"/ticket/update_priority/{ticket_pk}/{priority}/"
        response = self.client.put(
            url_update_ticket_priority,
            headers=result["headers"],
        )
        assert response.json == 204
        actual_priority = TicketModel.query.filter_by(pk=ticket_pk).first().priority
        self.assertEqual(actual_priority, priority)

    @patch.object(TranslateService, "translate", return_value="Some translated text")
    @patch.object(SendEmailService, "send_email", return_value=202)
    def test_update_ticket_status_pending_resolved(
        self, mocked_translate, mocked_send_email
    ):

        ticket_pk = self.create_ticket().json["pk"]
        result = self.assign_ticket(ticket_pk)
        headers = generate_headers(result["agent"])
        headers["Content-Type"] = "application/json"
        endpoints = (
            (
                "pending",
                {"resolution_text": "Need more info! Please update your ticket"},
                f"/ticket/{ticket_pk}/pending/",
            ),
            (
                "resolved",
                {
                    "resolution_text": "Your subscription doesn't cover this! Please pay more. Close your ticket!"
                },
                f"/ticket/{ticket_pk}/resolve/",
            ),
        )
        for expected_status, text, url in endpoints:
            response = self.client.put(url, headers=headers, json=text)
            assert response.json == 204
            actual_status = (
                TicketModel.query.filter_by(pk=ticket_pk).first().status.name
            )
            self.assertEqual(actual_status, expected_status)

    def test_update_description(self):
        ticket_pk = self.create_ticket().json["pk"]
        self.assign_ticket(ticket_pk)
        requester_id = TicketModel.query.filter_by(pk=ticket_pk).first().requester_id
        requester = RequesterUserModel.query.filter_by(pk=requester_id).first()
        headers = generate_headers(requester)
        headers["Content-Type"] = "application/json"
        url_update_ticket_description = f"/ticket/{ticket_pk}/description/"
        text = {
            "description": "I told you I don't have idea what the problem is. Just fix it!"
        }
        response = self.client.put(
            url_update_ticket_description, headers=headers, json=text
        )
        assert response.json == 204
        actual_description = (
            TicketModel.query.filter_by(pk=ticket_pk).first().description
        )
        expected_description = f"{TICKET_DATA['description']} | {text['description']}"
        self.assertEqual(actual_description, expected_description)

    def test_delete_ticket(self):
        ticket_pk = self.create_ticket().json["pk"]
        administrator = AdministratorUserFactory()
        headers = generate_headers(administrator)
        url_delete_ticket = f"/administrators/delete/{ticket_pk}/"
        response = self.client.delete(
            url_delete_ticket,
            headers=headers,
        )
        assert response.json == 204
        ticket = TicketModel.query.filter_by(pk=ticket_pk).first()
        self.assertEqual(None, ticket)

    def test_list_all_tickets(self):
        users = {
            "user_admin": AdministratorUserFactory(),
            "user_manager": ManagerUserFactory(),
            "user_agent": AgentUserFactory(),
            "user_requester": RequesterUserFactory(),
        }
        url_list_all_tickets = "/ticket/list/all/"

        for pk in range(TICKETS_CREATED):
            headers = generate_headers(users["user_requester"])
            headers["Content-Type"] = "application/json"
            ticket_pk = self.client.post(
                self.url_create_ticket,
                headers=headers,
                json=TICKET_DATA,
            ).json["pk"]
            TicketModel.query.filter_by(pk=ticket_pk).update(
                {
                    "manager_id": users["user_manager"].pk,
                    "agent_id": users["user_agent"].pk,
                }
            )
            db.session.commit()

        for k, v in users.items():
            headers = generate_headers(v)
            response = self.client.get(
                url_list_all_tickets,
                headers=headers,
            )
            self.assert200(response)
            tickets_listed = response.json
            self.assertEqual(TICKETS_CREATED, len(tickets_listed))

    def test_list_one_ticket_requester(self):
        ticket_pk = self.create_ticket().json["pk"]
        requester_id = TicketModel.query.filter_by(pk=ticket_pk).first().requester_id
        requester = RequesterUserModel.query.filter_by(pk=requester_id).first()
        headers = generate_headers(requester)
        url_list_one_ticket_requester = f"/ticket/list/{ticket_pk}/requester/"
        response = self.client.get(
            url_list_one_ticket_requester,
            headers=headers,
        )
        self.assert200(response)
        ticket_created = response.json
        self.assertEqual(ticket_created["title"], TICKET_DATA["title"])
        self.assertEqual(ticket_created["description"], TICKET_DATA["description"])
        self.assertEqual(TicketModel.query.count(), 1)
