from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.enums import TicketPriority
from schemas.base import BaseTicketSchema


class RequestTicketSchema(BaseTicketSchema):
    priority = EnumField(TicketPriority, by_value=False)


class RequestResolutionTextSchema(Schema):
    resolution_text = fields.String(required=True)


class RequestDescriptionSchema(Schema):
    description = fields.String(required=True)
