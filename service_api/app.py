from flask import Flask
from flask_cors import CORS
from service_api import api
from service_api.extensions import db, migrate


def create_app():

    """ Application factory, used to create application """

    app = Flask('service_api')
    app.config.from_object('service_api.config')

    CORS(app)
    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_extensions(app):

    """ Configure flask extensions """

    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):

    """ Register all blueprints for application """

    app.register_blueprint(api.views.blueprint)
