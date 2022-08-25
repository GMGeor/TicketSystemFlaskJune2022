from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes


class ProductionConfig:
    FLASK_ENV = "prod"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class DevelopmentConfig:
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


class TestConfig:
    """Configurations for Testing, with a separate test database."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('TES_DB_USER')}:{config('TES_DB_PASSWORD')}"
        f"@localhost:{config('TES_DB_PORT')}/{config('TES_DB_NAME')}"
    )


def create_app(configuration="config.DevelopmentConfig"):
    app = Flask(__name__)
    db.init_app(app)
    app.config.from_object(configuration)
    migrate = Migrate(app, db)
    api = Api(app)
    CORS(app)
    [api.add_resource(*route_data) for route_data in routes]
    return app
