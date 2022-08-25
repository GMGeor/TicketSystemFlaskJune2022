from flask import request
from flask_cors import cross_origin
from flask_restful import Resource

from managers.user import (
    RequesterManager,
    AgentManager,
    ManagerManager,
    AdministratorManager,
)
from schemas.request.users import RequestLoginUserSchema, RequestRegisterRequesterSchema
from utils.decorators import validate_schema


class CreateRequester(Resource):
    @validate_schema(RequestRegisterRequesterSchema)
    def post(self):
        data = request.get_json()
        token = RequesterManager.create(data)
        return {"token": token}, 201


class LoginRequester(Resource):
    @validate_schema(RequestLoginUserSchema)
    @cross_origin()
    def post(self):
        data = request.get_json()
        token = RequesterManager.login(data)
        return {"token": token, "role": "requester"}


class LoginAgent(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = AgentManager.login(data)
        return {"token": token, "role": "agent"}


class LoginManager(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = ManagerManager.login(data)
        return {"token": token, "role": "manager"}


class LoginAdministrator(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = AdministratorManager.login(data)
        return {"token": token, "role": "administrator"}
