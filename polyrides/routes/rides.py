"""Flask-RESTful resources for interacting with ride data."""
import flask_restful
from flask_restful import abort
from flask_restful import fields as flask_fields
from flask_restful import marshal_with

from webargs import fields as webargs_fields
from webargs.flaskparser import parser
from webargs.flaskparser import use_args

from polyrides.models.user import Ride

# Fields to include in a response body.
_response_schema = {  # pylint: disable=C0103
    'id': flask_fields.Integer
    # Other Ride fields go here.
}

_request_schema = {  # pylint: disable=C0103
    # Ride fields go here.
}


@parser.error_handler
def _handle_parse_error(err, req, schema):
    """Handler for request parse errors.

    This is called if a method decorated with `use_args` encounters a parse error.

    Args:
        err (webargs.core.ValidationError): Raised error.
        req (flask.Request): Flask request object.
        schema (marshmallow.Schema): Schema used to parse request.
    """
    abort(400, message=err.messages)


class Rides(flask_restful.Resource):
    """Resource for interacting with `Ride` data."""
    pass


class RideById(flask_restful.Resource):
    """Resource for interacting with `User` data by id."""
    pass
