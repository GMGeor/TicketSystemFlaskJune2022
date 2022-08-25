from marshmallow import Schema, fields, validate


class BaseAuthSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=8, max=20))


class BaseTicketSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
