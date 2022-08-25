from random import randint

import factory

from db import db
from models import (
    TicketModel,
    UserRole,
    RequesterUserModel,
    AgentUserModel,
    ManagerUserModel,
    AdministratorUserModel,
)


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class RequesterUserFactory(BaseFactory):
    class Meta:
        model = RequesterUserModel

    pk = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = str(randint(100000, 200000))
    password = factory.Faker("password")
    role = UserRole.requester


class AgentUserFactory(BaseFactory):
    class Meta:
        model = AgentUserModel

    pk = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = str(randint(100000, 200000))
    password = factory.Faker("password")
    role = UserRole.agent


class ManagerUserFactory(BaseFactory):
    class Meta:
        model = ManagerUserModel

    pk = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = str(randint(100000, 200000))
    password = factory.Faker("password")
    role = UserRole.manager


class AdministratorUserFactory(BaseFactory):
    class Meta:
        model = AdministratorUserModel

    pk = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = str(randint(100000, 200000))
    password = factory.Faker("password")
    role = UserRole.administrator


class TicketFactory(BaseFactory):
    class Meta:
        model = TicketModel

    pk = factory.Sequence(lambda n: n)
    title = "Ticket's title"
    description = "Ticket's description"
    requester_id = factory.Sequence(lambda n: n)
