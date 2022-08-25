from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import ExpiredSignatureError, InvalidTokenError
from werkzeug.exceptions import Unauthorized

# Keep this imports because of the eval function
from models.users import RequesterUserModel, AgentUserModel, ManagerUserModel, AdministratorUserModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.pk,
            "exp": datetime.utcnow() + timedelta(days=20000),
            "type": user.__class__.__name__,
        }
        return jwt.encode(payload, key=config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        if not token:
            raise Unauthorized("Missing token!")
        try:
            payload = jwt.decode(
                jwt=token, key=config("SECRET_KEY"), algorithms=["HS256"]
            )
            return payload["sub"], payload["type"]
        except ExpiredSignatureError:
            raise Unauthorized("Token expired!")
        except InvalidTokenError:
            raise Unauthorized("Invalid token!")


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    user_id, type_user = AuthManager.decode_token(token)
    return eval(f"{type_user}.query.filter_by(pk={user_id}).first()")
