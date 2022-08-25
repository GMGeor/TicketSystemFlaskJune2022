from db import db
from models.enums import UserRole, UserPreferredLanguage


class BaseUserModel(db.Model):
    __abstract__ = True

    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    phone = db.Column(db.String(14), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class RequesterUserModel(BaseUserModel):
    __tablename__ = "requesters"

    tickets = db.relationship("TicketModel", backref="ticket", lazy="dynamic")
    role = db.Column(db.Enum(UserRole), default=UserRole.requester, nullable=False)
    preferred_language = db.Column(
        db.Enum(UserPreferredLanguage), default=UserPreferredLanguage.en
    )


class AgentUserModel(BaseUserModel):
    __tablename__ = "agents"

    manager_id = db.Column(db.Integer, db.ForeignKey("managers.pk"))
    manager = db.relationship("ManagerUserModel")
    assigned_tickets = db.relationship(
        "TicketModel", backref="assigned_ticket", lazy="dynamic"
    )
    role = db.Column(db.Enum(UserRole), default=UserRole.agent, nullable=False)


class ManagerUserModel(BaseUserModel):
    __tablename__ = "managers"

    administrator_id = db.Column(db.Integer, db.ForeignKey("administrators.pk"))
    administrator = db.relationship("AdministratorUserModel")
    agents = db.relationship("AgentUserModel", backref="agent", lazy="dynamic")
    role = db.Column(db.Enum(UserRole), default=UserRole.manager, nullable=False)


class AdministratorUserModel(BaseUserModel):
    __tablename__ = "administrators"

    managers = db.relationship("ManagerUserModel", backref="manager", lazy="dynamic")
    role = db.Column(db.Enum(UserRole), default=UserRole.administrator, nullable=False)
