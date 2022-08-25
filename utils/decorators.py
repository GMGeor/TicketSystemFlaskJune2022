from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import auth
from models.enums import TicketPriority
from models.ticket import TicketModel
from models.users import AgentUserModel


def validate_schema(schema_name):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if not errors:
                return func(*args, **kwargs)
            raise BadRequest(errors)

        return wrapper

    return decorated_function


def permission_required(role):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if not current_user.role == role:
                raise Forbidden("Permission denied!")
            return func(*args, **kwargs)

        return wrapper

    return decorated_function


def validate_ticket_exists():
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            if not TicketModel.query.filter_by(pk=kwargs["pk"]).first():
                raise BadRequest("No such ticket!")
            return func(*args, **kwargs)

        return wrapper

    return decorated_function


def validate_agent_exists():
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            if not AgentUserModel.query.filter_by(pk=kwargs["agent_id"]).first():
                raise BadRequest("No such agent!")
            return func(*args, **kwargs)

        return wrapper

    return decorated_function


def validate_priority():
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            names = [member.name for member in TicketPriority]
            if kwargs["priority"] not in names:
                raise BadRequest("Invalid data input!")
            return func(*args, **kwargs)

        return wrapper

    return decorated_function


def validate_ticket_created_by_requester():
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            ticket = TicketModel.query.filter_by(pk=kwargs["pk"]).first()
            if not auth.current_user().pk == ticket.requester_id:
                raise Forbidden("You didn't create this ticket!")
            return func(*args, **kwargs)

        return wrapper

    return decorated_function
