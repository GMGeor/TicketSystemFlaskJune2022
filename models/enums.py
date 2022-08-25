from enum import Enum


class UserRole(Enum):
    administrator = "Administrator"
    manager = "Manager"
    agent = "Agent"
    requester = "Requester"


class UserPreferredLanguage(Enum):
    bg = "BG"
    it = "IT"
    de = "DE"
    fr = "FR"
    en = "EN"


class TicketState(Enum):
    new = "New"
    open = "Open"
    pending = "Pending"
    resolved = "Resolved"
    closed = "Closed"


class TicketPriority(Enum):
    low = "Low"
    normal = "Normal"
    high = "High"
    urgent = "Urgent"
