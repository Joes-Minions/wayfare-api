"""Flask-RESTful resources for interacting with ride data."""
import flask_restful
from flask_restful import abort
from flask_restful import fields as flask_fields
from flask_restful import marshal_with
from webargs import fields as webargs_fields
from webargs.flaskparser import parser
from webargs.flaskparser import use_args

import dateutil.parser

from wayfare.exceptions import InvalidCapacityError
from wayfare.models import Passenger

BASE_URL = '/rides'

# Fields to include in a response body.
_response_schema = {  # pylint: disable=C0103
    'id': flask_fields.Integer,
    'user_id': flask_fields.Integer,
    'ride_id': flask_fields.Integer,
    'status_id': flask_fields.Integer
}

_request_schema = {  # pylint: disable=C0103
    # Passenger fields go here.
    'ride_id': flask_fields.Integer
}

def _make_request_schema(require_all: bool = False) -> dict:
    """Create an expected schema for a request body or query.

    Args:
        require_all (bool): True to require that all fields be present.
    """

    return {
        'user_id': webargs_fields.Integer(required=require_all),  # pylint: disable=E1101
        #'ride_id': webargs_fields.Integer(required=require_all),  # pylint: disable=E1101
        'status_id': webargs_fields.Integer(required=require_all),  # pylint: disable=E1101
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


class Passengers(flask_restful.Resource):
    """Resource for interacting with `Passenger` data."""
    @marshal_with(_response_schema)
    def get(self):
        """Retrieve all passengers.

        NOTE: This method can be very memory-intensive and should not be used in production.
        """
        return list(Passenger.get_all())

    @use_args(_make_request_schema(require_all=True))
    def post(self, ride_id: int, request_body: dict):
        """Create a passenger.

        Args:
            request_body (dict): Data extracted from request body.
        """
        print('ride_id: ' + str(ride_id)))
        try:
            passenger = Passenger(
                user_id=request_body['user_id'],
                ride_id=ride_id,
                status_id=request_body['status_id']
            )
            passenger.create()
            return '', 201, {'location': f'{BASE_URL}/{passenger.ride_id}/users/{passenger.user_id}'}
        except InvalidCapacityError as ex:
            abort(400, message=ex.message)


    def delete(self):
        """Delete all passengers.

        NOTE: This is (potentially) an incredibly destructive method. Be careful.
        """
        Passenger.delete_all()
        return '', 200


class PassengersById(flask_restful.Resource):
    """Resource for interacting with ride data based on a ride id."""
    @marshal_with(_response_schema)
    def get(self, ride_id: int, user_id: int):
        """Get a passenger resource by id.

        Args:
            ride_id (int): id of the ride for passenger
            user_id (int): id of passenger (user)

        Returns:
            Passenger with the given ids if found.
        """
        passenger = Passenger.find_by_id(ride_id, user_id)
        if not passenger:
            abort(404, message="Ride {} does not exist".format(ride_id))
        return passenger

    # TODO: This method should not require all fields.
    @use_args(_make_request_schema(require_all=True))
    def put(self, request_body: dict, ride_id: int):
        """Create or update a ride resource by id.

        Args:
            request_body (dict): Data extracted from request body.
            ride_id (int): ride id provided in the uri path.
        """
        passenger = Passenger.find_by_id(ride_id)
        if ride:
            ride.update(request_body)
            return '', 200
        ride = Ride(**request_body)
        ride.create()
        return '', 201

    def delete(self, ride_id: int):
        """Delete ride with the given id.

        Args:
            ride_id (int): id of the ride to delete
        """
        ride = Ride.find_by_id(ride_id)
        if ride:
            ride.delete_instance()
            return '', 200
        abort(404, message="Ride {} does not exist".format(ride_id))
