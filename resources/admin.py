from flask import request
from flask_restful import Resource

from managers.auth import auth
from managers.ticket import TicketManager
from managers.user import AdministratorManager, ManagerManager, AgentManager
from models import UserRole
from schemas.request.users import (
    RequestRegisterAdministratorSchema,
    RequestRegisterManagerSchema,
    RequestRegisterAgentSchema,
)
from utils.decorators import (
    validate_schema,
    permission_required,
    validate_ticket_exists,
)


class CreateAdministrator(Resource):
    @auth.login_required
    @permission_required(UserRole.administrator)
    @validate_schema(RequestRegisterAdministratorSchema)
    def post(self):
        data = request.get_json()
        AdministratorManager.create(data)
        return 201


class CreateManager(Resource):
    @auth.login_required
    @permission_required(UserRole.administrator)
    @validate_schema(RequestRegisterManagerSchema)
    def post(self):
        data = request.get_json()
        ManagerManager.create(data)
        return 201


class CreateAgent(Resource):
    @auth.login_required
    @permission_required(UserRole.administrator)
    @validate_schema(RequestRegisterAgentSchema)
    def post(self):
        data = request.get_json()
        AgentManager.create(data)
        return 201


class DeleteTicket(Resource):
    @auth.login_required
    @permission_required(UserRole.administrator)
    @validate_ticket_exists()
    def delete(self, pk):
        TicketManager.delete(pk)
        return 204
