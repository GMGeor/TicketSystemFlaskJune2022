from resources.admin import (
    CreateAdministrator,
    CreateManager,
    CreateAgent,
    DeleteTicket,
)
from resources.auth import (
    CreateRequester,
    LoginRequester,
    LoginAdministrator,
    LoginManager,
    LoginAgent,
)
from resources.ticket import (
    TicketListAll,
    TicketListOneRequester,
    TicketCreate,
    AssignTicket,
    UpdatePriority,
    PendingTicket,
    ResolveTicket,
    UpdateDescription,
    CloseTicket,
)


routes = (
    (CreateRequester, "/auth/register/"),
    (LoginRequester, "/auth/login/"),
    (LoginManager, "/auth/managers/login/"),
    (LoginAgent, "/auth/agents/login/"),
    (LoginAdministrator, "/auth/administrators/login/"),
    (CreateAdministrator, "/administrators/create/administrator/"),
    (CreateManager, "/administrators/create/manager/"),
    (CreateAgent, "/administrators/create/agent/"),
    (DeleteTicket, "/administrators/delete/<int:pk>/"),
    (TicketListAll, "/ticket/list/all/"),
    (TicketListOneRequester, "/ticket/list/<int:pk>/requester/"),
    (TicketCreate, "/ticket/create/"),
    (AssignTicket, "/ticket/assign/<int:pk>/<int:agent_id>/"),
    (UpdatePriority, "/ticket/update_priority/<int:pk>/<string:priority>/"),
    (PendingTicket, "/ticket/<int:pk>/pending/"),
    (ResolveTicket, "/ticket/<int:pk>/resolve/"),
    (UpdateDescription, "/ticket/<int:pk>/description/"),
    (CloseTicket, "/ticket/<int:pk>/close/"),
)
