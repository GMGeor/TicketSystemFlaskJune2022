from marshmallow import fields
from marshmallow_enum import EnumField

from models.enums import UserRole
from schemas.base import BaseAuthSchema


class RequestRegisterUserSchema(BaseAuthSchema):
    first_name = fields.String(min_length=2, max_length=20, required=True)
    last_name = fields.String(min_length=2, max_length=20, required=True)
    phone = fields.String(min_length=10, max_length=13, required=True)


class RequestRegisterRequesterSchema(RequestRegisterUserSchema):
    # TODO check it improve it
    role = EnumField(UserRole, by_value=True)


class RequestRegisterAgentSchema(RequestRegisterUserSchema):
    # TODO check it improve it
    role = EnumField(UserRole, by_value=True)
    manager_id = fields.Integer(required=True)


class RequestRegisterAdministratorSchema(RequestRegisterUserSchema):
    # TODO check it improve it
    role = EnumField(UserRole, by_value=True)


class RequestRegisterManagerSchema(RequestRegisterUserSchema):
    # TODO check it improve it
    role = EnumField(UserRole, by_value=True)
    administrator_id = fields.Integer(required=True)


class RequestLoginUserSchema(BaseAuthSchema):
    pass
