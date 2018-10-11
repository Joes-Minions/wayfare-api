"""Endpoint for interacting with user data.

Provides the following endpoints and methods:

    /users/
    - GET : Get all users (admin only).
    - POST: Create a user.

    /users/{user_id}/
"""
import json

from typing import Dict, List

from flask import jsonify
from flask_restful import reqparse, Resource

from polyrides.data.json_wrapper import JsonWrapper


def _parse_request() -> Dict:
    """Parse the JSON body of an HTTP POST request."""
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        help="The user's given name.")
    parser.add_argument('last_name',
                        type=str,
                        help="The user's family name.")
    parser.add_argument('email',
                        type=str,
                        help="The user's email address.")
    parser.add_argument('password',
                        type=str,
                        help="The user's chosen password.")
    return parser.parse_args()


class Users(Resource):
    """Resource for interacting with user data."""

    def __init__(self):
        """Initialize the Resource, loading data from the source (which in this case is a JSON file)."""
        self.data = JsonWrapper('users')

    def get(self):
        """Retrieve all users from the data source."""
        return jsonify(self.data.read())

    def post(self):
        """Add a user to the data source."""
        user = _parse_request()
        try:
            if not user['first_name']:
                raise Exception('Required field: "first_name".')
            if not user['last_name']:
                raise Exception('Required field: "last_name".')
            if not user['email']:
                raise Exception('Required field: "email".')
            if not user['password']:
                raise Exception('Required field: "password".')
            if self.data.find(lambda item: item['email'] == user['email']):
                raise Exception('Duplicate email: "{}".'.format(user['email']))

            self.data.create(user)
            return '', 201
        except Exception as err:
            return str(err), 400
