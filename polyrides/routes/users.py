"""Endpoint for interacting with user data.

Provides the following endpoints and methods:

    /users/
    - GET : Get all users.
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


class UserDAO(JsonWrapper):
    """Data Access Object that provides methods for interacting with user data contained in a JSON file."""

    def __init__(self):
        super().__init__('users')

    def create_user(self, user: dict):
        """Add a user to the data source, generating an id for the user.

        Args:
            user (dict): A dictionary representation of a user.
        """
        if not self.all_users():  # Set the first user's ID to 1.
            new_user_id = 1
        else:                     # This will reuse an ID if the most recently added user is deleted, but who cares?
            all_user_ids = [user['id'] for user in self.all_users()]
            max_id = max(all_user_ids)
            new_user_id = max_id + 1
        user['id'] = new_user_id
        self.create(user)

    def find_user_by_id(self, user_id: int) -> dict:
        """Search the data source for a user with the given id.
        Returns None if no matches are found.
        
        Args:
            user_id (int): User ID to look up.
        
        Returns:
            (dict) User with the given ID if found.
        """
        return self.find(lambda user: user['id'] == user_id)

    def find_user_by_email(self, email: str) -> dict:
        """Search the data source for a user with the given email.
        Returns None if no matches are found.
        
        Args:
            email (str): User email address to look up.
        
        Returns:
            (dict) User with the given email if found.
        """
        return self.find(lambda user: user['email'] == email)

    def find_users_with_first_name(self, name: str) -> list:
        """Search the data source for all users with the given first name.
        Returns an empty list if no matches are found.
        
        Args:
            name (str): First name to search for.
        
        Returns:
            (list) List of all users with the given first name.
        """
        return self.find(lambda user: user['first_name'] == name)

    def find_users_with_last_name(self, name: str) -> list:
        """Search the data source for all users with the given last name.
        Returns an empty list if no matches are found.
        
        Args:
            name (str): Last name to search for.
        
        Returns:
            (list) List of all users with the given last name.
        """
        return self.find(lambda user: user['last_name'] == name)

    def all_users(self) -> list:
        """Retrieve all user objects from the data source.

        Returns:
            (list) All users stored in the data source.
        """
        return self.read()


class Users(Resource):
    """Resource for interacting with user data."""

    def __init__(self):
        """Initialize the Resource, creating a database-like interface to the user data."""
        self.db = UserDAO()

    def get(self):
        """Retrieve all user resources."""
        return jsonify(self.db.all_users())

    def post(self):
        """Add a user resource.

        All of the following fields are required for a user object:
        - first_name
        - last_name
        - email  -- must be unique
        - password
        """
        user = _parse_request()
        try:
            if not user['first_name']:
                raise Exception("Missing field: 'first_name'")
            if not user['last_name']:
                raise Exception("Missing field: 'last_name'")
            if not user['email']:
                raise Exception("Missing field: 'email'")
            if not user['password']:
                raise Exception("Missing field: 'password'")
            if self.db.find_user_by_email(user['email']):
                raise Exception("Duplicate email: '{}'".format(user['email']))

            self.db.create_user(user)
            return '', 201
        except Exception as err:
            return str(err), 400

    def delete(self):
        """Delete all user resources."""
        self.db.nuke()
