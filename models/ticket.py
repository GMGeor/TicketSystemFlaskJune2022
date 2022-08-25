from sqlalchemy import func

from db import db
from models.enums import TicketState, TicketPriority


class TicketModel(db.Model):
    __tablename__ = "tickets"

    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    resolution_text = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime, server_default=func.now())
    last_update_on = db.Column(db.DateTime, onupdate=func.now())
    closed_on = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum(TicketState), default=TicketState.new)
    priority = db.Column(db.Enum(TicketPriority), default=TicketPriority.low)
    requester_id = db.Column(db.Integer, db.ForeignKey("requesters.pk"), nullable=False)
    requester = db.relationship("RequesterUserModel")
    agent_id = db.Column(db.Integer, db.ForeignKey("agents.pk"), nullable=True)
    agent = db.relationship("AgentUserModel")
    manager_id = db.Column(db.Integer, db.ForeignKey("managers.pk"), nullable=True)
    manager = db.relationship("ManagerUserModel")
