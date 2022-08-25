from flask import request
from flask_api import status
from flask_restful import Resource

from managers.auth import auth
from managers.ticket import TicketManager
from models.enums import UserRole
from schemas.request.ticket import (
    RequestTicketSchema,
    RequestResolutionTextSchema,
    RequestDescriptionSchema,
)
from schemas.response.ticket import ResponseTicketSchema
from utils.decorators import (
    permission_required,
    validate_schema,
    validate_ticket_exists,
    validate_agent_exists,
    validate_priority,
    validate_ticket_created_by_requester,
)


class TicketListAll(Resource):
    @auth.login_required
    def get(self):
        user = auth.current_user()
        tickets = TicketManager.get_all_tickets(user)
        # Use dump, not load when schema and object are not the same
        return ResponseTicketSchema().dump(tickets, many=True)


class TicketListOneRequester(Resource):
    @auth.login_required
    @permission_required(UserRole.requester)
    @validate_ticket_exists()
    @validate_ticket_created_by_requester()
    def get(self, pk):
        ticket = TicketManager.get_one_ticket(pk)
        return ResponseTicketSchema().dump(ticket)


class TicketCreate(Resource):
    @auth.login_required
    @permission_required(UserRole.requester)
    @validate_schema(RequestTicketSchema)
    def post(self):
        requester = auth.current_user()
        data = request.get_json()
        ticket = TicketManager.create(data, requester)
        # Use dump, not load when schema and object are not the same
        return ResponseTicketSchema().dump(ticket), status.HTTP_201_CREATED


class AssignTicket(Resource):
    @auth.login_required
    @permission_required(UserRole.manager)
    @validate_ticket_exists()
    @validate_agent_exists()
    def put(self, pk, agent_id):
        TicketManager.assign(pk, agent_id)
        return status.HTTP_204_NO_CONTENT


class UpdatePriority(Resource):
    @auth.login_required
    @permission_required(UserRole.manager)
    @validate_ticket_exists()
    @validate_priority()
    def put(self, pk, priority):
        TicketManager.priority(pk, priority)
        return status.HTTP_204_NO_CONTENT


class PendingTicket(Resource):
    @auth.login_required
    @permission_required(UserRole.agent)
    @validate_ticket_exists()
    @validate_schema(RequestResolutionTextSchema)
    def put(self, pk):
        data = request.get_json()
        text = data["resolution_text"]
        TicketManager.pending(pk, text)
        return status.HTTP_204_NO_CONTENT


class ResolveTicket(Resource):
    @auth.login_required
    @permission_required(UserRole.agent)
    @validate_ticket_exists()
    @validate_schema(RequestResolutionTextSchema)
    def put(self, pk):
        data = request.get_json()
        text = data["resolution_text"]
        TicketManager.resolve(pk, text)
        return status.HTTP_204_NO_CONTENT


class UpdateDescription(Resource):
    @auth.login_required
    @permission_required(UserRole.requester)
    @validate_ticket_exists()
    @validate_ticket_created_by_requester()
    @validate_schema(RequestDescriptionSchema)
    def put(self, pk):
        data = request.get_json()
        text = data["description"]
        TicketManager.update_description(pk, text)
        return status.HTTP_204_NO_CONTENT


class CloseTicket(Resource):
    @auth.login_required
    @permission_required(UserRole.requester)
    @validate_ticket_exists()
    @validate_ticket_created_by_requester()
    def put(self, pk):
        TicketManager.close(pk)
        return status.HTTP_204_NO_CONTENT
