from flask_testing import TestCase

from config import create_app
from db import db
from tests.factories import (
    RequesterUserFactory,
    AgentUserFactory,
    AdministratorUserFactory,
    ManagerUserFactory,
    TicketFactory,
)
from tests.helpers import generate_headers

EMAIL = "g_mg@abv.bg"
EXPIRED_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjAsImV4cCI6LTY2NzA4NzgyLCJ0eXBlIjoiUmVxdWVzdGVyVXNlck1vZGVsIn0.8_IXotCPzttUPv85kY285yks6jk6L8aVLnPeEQpz-zM"
ENDPOINTS_DATA = [
    ("POST", "/administrators/create/administrator/"),
    ("POST", "/administrators/create/manager/"),
    ("POST", "/administrators/create/agent/"),
    ("DELETE", "/administrators/delete/1/"),
    ("GET", "/ticket/list/all/"),
    ("POST", "/ticket/create/"),
    ("PUT", "/ticket/assign/1/1/"),
    ("PUT", "/ticket/update_priority/1/low/"),
    ("PUT", "/ticket/1/pending/"),
    ("PUT", "/ticket/1/resolve/"),
    ("PUT", "/ticket/1/description/"),
    ("PUT", "/ticket/1/close/"),
]


class TestApplication(TestCase):
    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def iterate_endpoints(
        self, endpoints_data, status_code_method, expected_response_body, text=None
    ):
        response = None
        if not text:
            text = {}
        for header, method, url in endpoints_data:
            if method == "POST":
                response = self.client.post(
                    url,
                    headers=header,
                    json=text,
                )
            elif method == "GET":
                response = self.client.get(
                    url,
                    headers=header,
                )
            elif method == "PUT":
                response = self.client.put(
                    url,
                    headers=header,
                    json=text,
                )
            elif method == "DELETE":
                response = self.client.delete(
                    url,
                    headers=header,
                )
            status_code_method(response)
            self.assertEqual(response.json, expected_response_body)

    def test_login_required(self):
        headers = {}
        endpoints_with_headers = [(headers, *e) for e in ENDPOINTS_DATA]
        self.iterate_endpoints(
            endpoints_with_headers, self.assert401, {"message": "Missing token!"}
        )

    def test_invalid_token_raises(self):
        headers = {"Authorization": "Bearer inval1dt0ken"}
        endpoints_with_headers = [(headers, *e) for e in ENDPOINTS_DATA]
        self.iterate_endpoints(
            endpoints_with_headers, self.assert401, {"message": "Invalid token!"}
        )

    def test_expired_token_raises(self):
        RequesterUserFactory()
        headers = {"Authorization": f"Bearer {EXPIRED_TOKEN}"}
        endpoints_with_headers = [(headers, *e) for e in ENDPOINTS_DATA]
        self.iterate_endpoints(
            endpoints_with_headers, self.assert401, {"message": "Token expired!"}
        )

    def test_missing_permissions_for_manager_raises(self):
        user = RequesterUserFactory()
        headers = generate_headers(user)
        endpoints = (
            (headers, "PUT", "/ticket/assign/1/1/"),
            (headers, "PUT", "/ticket/update_priority/1/low/"),
        )
        self.iterate_endpoints(
            endpoints, self.assert403, {"message": "Permission denied!"}
        )
        del user, headers

    def test_missing_permissions_for_admin_raises(self):
        headers = generate_headers(RequesterUserFactory())
        endpoints = (
            (headers, "POST", "/administrators/create/administrator/"),
            (headers, "POST", "/administrators/create/manager/"),
            (headers, "POST", "/administrators/create/agent/"),
            (headers, "DELETE", "/administrators/delete/1/"),
        )
        self.iterate_endpoints(
            endpoints, self.assert403, {"message": "Permission denied!"}
        )
        del headers

    def test_missing_permissions_for_agent_raises(self):
        headers = generate_headers(RequesterUserFactory())
        endpoints = (
            (headers, "PUT", "/ticket/1/pending/"),
            (headers, "PUT", "/ticket/1/resolve/"),
        )
        self.iterate_endpoints(
            endpoints, self.assert403, {"message": "Permission denied!"}
        )
        del headers

    def test_missing_permissions_for_requester_raises(self):
        headers = generate_headers(AgentUserFactory())
        endpoints = (
            (headers, "POST", "/ticket/create/"),
            (headers, "PUT", "/ticket/1/description/"),
            (headers, "PUT", "/ticket/1/close/"),
        )
        self.iterate_endpoints(
            endpoints, self.assert403, {"message": "Permission denied!"}
        )
        del headers

    def test_validate_ticket_exists(self):
        headers_auth_agent = generate_headers(AgentUserFactory())
        headers_auth_requester = generate_headers(RequesterUserFactory())
        headers_auth_manager = generate_headers(ManagerUserFactory())
        headers_auth_administrator = generate_headers(AdministratorUserFactory())
        endpoints = (
            (headers_auth_manager, "PUT", "/ticket/assign/1/1/"),
            (headers_auth_manager, "PUT", "/ticket/update_priority/1/low/"),
            (headers_auth_agent, "PUT", "/ticket/1/pending/"),
            (headers_auth_agent, "PUT", "/ticket/1/resolve/"),
            (headers_auth_requester, "PUT", "/ticket/1/description/"),
            (headers_auth_requester, "PUT", "/ticket/1/close/"),
            (headers_auth_administrator, "DELETE", "/administrators/delete/1/"),
        )
        self.iterate_endpoints(
            endpoints, self.assert400, {"message": "No such ticket!"}
        )
        del (
            headers_auth_agent,
            headers_auth_requester,
            headers_auth_manager,
            headers_auth_administrator,
        )

    def test_validate_ticket_created_by_requester(self):
        RequesterUserFactory(pk=0)  # create user with pk = 0
        TicketFactory(pk=0, requester_id=0)  # create a ticket, with requester_id = 0
        user = RequesterUserFactory(
            pk=1
        )  # create another user, with pk = 1 so why it is not the owner of the ticket
        headers = generate_headers(user)
        headers["Content-Type"] = "application/json"
        endpoints = (
            (headers, "PUT", "/ticket/0/description/"),
            (headers, "PUT", "/ticket/0/close/"),
        )
        self.iterate_endpoints(
            endpoints, self.assert403, {"message": "You didn't create this ticket!"}
        )

    def test_missing_required_field_schema_request_ticket_schema_raises(self):
        user = RequesterUserFactory()
        headers = generate_headers(user)
        headers["Content-Type"] = "application/json"
        text = {"title": "Huge Problem"}
        endpoints = ((headers, "POST", "/ticket/create/"),)
        self.iterate_endpoints(
            endpoints,
            self.assert400,
            {"message": {"description": ["Missing data for required field."]}},
            text,
        )

    def test_unknown_field_schema_request_ticket_schema_raises(self):
        user = RequesterUserFactory()
        headers = generate_headers(user)
        headers["Content-Type"] = "application/json"
        text = {
            "title": "Huge Problem",
            "description": "Can't implement the integration I wanted",
            "some_additional_field": "that is not needed",
        }
        endpoints = ((headers, "POST", "/ticket/create/"),)
        self.iterate_endpoints(
            endpoints,
            self.assert400,
            {"message": {"some_additional_field": ["Unknown field."]}},
            text,
        )

    def test_not_valid_string_schema_request_resolution_text_schema_raises(self):
        RequesterUserFactory(pk=0)
        user = AgentUserFactory()
        headers = generate_headers(user)
        ticket = TicketFactory(requester_id=0)
        ticket_pk = ticket.pk
        headers["Content-Type"] = "application/json"
        text = {"resolution_text": 4}
        endpoints = (
            (headers, "PUT", f"/ticket/{ticket_pk}/pending/"),
            (headers, "PUT", f"/ticket/{ticket_pk}/resolve/"),
        )
        self.iterate_endpoints(
            endpoints,
            self.assert400,
            {"message": {"resolution_text": ["Not a valid string."]}},
            text,
        )
