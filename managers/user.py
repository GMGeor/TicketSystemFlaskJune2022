from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from managers.auth import AuthManager
from models.users import (
    RequesterUserModel,
    AgentUserModel,
    ManagerUserModel,
    AdministratorUserModel,
)


def register(user_data, user_model):
    """
    Hashes the plain password
    :param user_model: obj
    :param user_data: dict
    :return: token
    """
    user_data["password"] = generate_password_hash(
        user_data["password"], method="sha256"
    )
    user = user_model(**user_data)
    try:
        db.session.add(user)
        db.session.flush()
        return AuthManager.encode_token(user)
    except Exception as ex:
        raise BadRequest(str(ex))


def sign_in(user_data, user_model):
    """
    Checks the email and password (hashes the plain password)
    :param user_model: obj
    :param user_data: dict -> email, password
    :return: token
    """
    try:
        user = user_model.query.filter_by(email=user_data["email"]).first()
        if user and check_password_hash(user.password, user_data["password"]):
            return AuthManager.encode_token(user)
        raise Exception
    except Exception:
        raise BadRequest("Invalid username or password")


class RequesterManager:
    @staticmethod
    def create(requester_data):
        return register(requester_data, RequesterUserModel)

    @staticmethod
    def login(requester_data):
        return sign_in(requester_data, RequesterUserModel)


class AgentManager:
    @staticmethod
    def create(agent_data):
        return register(agent_data, AgentUserModel)

    @staticmethod
    def login(agent_data):
        return sign_in(agent_data, AgentUserModel)


class AdministratorManager:
    @staticmethod
    def create(administrator_data):
        return register(administrator_data, AdministratorUserModel)

    @staticmethod
    def login(administrator_data):
        return sign_in(administrator_data, AdministratorUserModel)


class ManagerManager:
    @staticmethod
    def create(manager_data):
        return register(manager_data, ManagerUserModel)

    @staticmethod
    def login(manager_data):
        return sign_in(manager_data, ManagerUserModel)
