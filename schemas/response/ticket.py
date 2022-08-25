from marshmallow import fields
from marshmallow_enum import EnumField

from models.enums import TicketState, TicketPriority
from schemas.base import BaseTicketSchema


class ResponseTicketSchema(BaseTicketSchema):
    pk = fields.Integer(required=True)
    status = EnumField(TicketState)
    priority = EnumField(TicketPriority)
    created_on = fields.DateTime(required=True)
