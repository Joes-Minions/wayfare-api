"""Endpoint for interacting with user data.

Provides the following endpoints and methods:

    /users/
    - GET : Get all users.
    - POST: Create a user.

    /users/{user_id}/
"""
import flask
import flask_restful

from flask_restful import reqparse

from polyrides.data.dao import UserDAO


def _parse_user_from_request_body(require_all_fields: bool = False) -> dict:
    """Parse user data from a request body provided in a POST or PUT request.

    Args:
        require_all_fields (bool): True to require that all fields be present in the request body.

    Returns:
        (dict) User data fields as a dictionary.
    """
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('first_name',
                        type=str,
                        help="Missing field: 'first_name'",
                        required=require_all_fields)
    parser.add_argument('last_name',
                        type=str,
                        help="Missing field: 'last_name'",
                        required=require_all_fields)
    parser.add_argument('email',
                        type=str,
                        help="Missing field: 'email'",
                        required=require_all_fields)
    parser.add_argument('password',
                        type=str,
                        help="Missing field: 'password'",
                        required=require_all_fields)
    return parser.parse_args()


class Users(flask_restful.Resource):
    """Resource for interacting with all user data."""

    def __init__(self):
        """Initialize the Resource, creating a database-like interface to the user data."""
        self.db = UserDAO()

    def get(self):
        """Retrieve all user resources."""
        all_users = self.db.all_users()
        return flask.jsonify(all_users)

    def post(self):
        """Add a user resource."""
        user = _parse_user_from_request_body(require_all_fields=True)
        try:
            if self.db.find_user_by_email(user.email):
                raise Exception("Duplicate email: '{}'".format(user.email))

            self.db.create_user(user)
            return '', 201
        except Exception as err:
            error_message = {
                'message': str(err)
            }
            return error_message, 400

    def delete(self):
        """Delete all user resources."""
        self.db.nuke()


class UserById(flask_restful.Resource):
    """Resource for interacting with user data given a user ID."""
    def __init__(self):
        """Initialize the Resource, creating a database-like interface to the user data."""
        self.db = UserDAO()

    def get(self, user_id: int) -> dict:
        """Retrieve user with the given ID.

        Args:
            user_id (int): ID of the user to fetch.

        Returns:
            (dict): User with the given ID as a dictionary.
        """
        user = self.db.find_user_by_id(user_id)
        if not user:
            return '', 404
        return flask.jsonify(user)

    def put(self, user_id: int):
        """Update user with the given ID.

        Args:
            user_id (int): ID of the user to replace.
        """
        user = self.db.find_user_by_id(user_id)
        if not user:
            return '', 404
        query_params = _parse_user_from_request_body(require_all_fields=False)
        updated_user = {key: query_params.get(key) or user[key] for key in user}
        self.db.update_user(updated_user, user_id)
        return '', 200

    def delete(self, user_id: int):
        """Delete user with the given ID.

        Args:
            user_id (int): ID of the user to delete.
        """
        user = self.db.find_user_by_id(user_id)
        if not user:
            return '',404
        self.db.del_user_by_id(user_id)
        return '',200
