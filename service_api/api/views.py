from flask import jsonify
from flask import Blueprint
from flask_restful import Api
from marshmallow import ValidationError
from service_api.api.resources import *

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)


api.add_resource(UserResource, '/user', endpoint='user')
api.add_resource(UserToken, '/login', endpoint='user-check')


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
