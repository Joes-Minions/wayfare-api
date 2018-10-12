"""Endpoint for interacting with user data.

Provides the following endpoints and methods:

    /users/
    - GET : Get all users.
    - POST: Create a user.

    /users/{user_id}/
"""
import flask
import flask_restful
import json

from flask_restful import reqparse

from polyrides.data.json_wrapper import JsonWrapper


def _parse_user(require_all_fields: bool = False) -> dict:
    """Parse a user from a request."""
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('first_name', type=str, required=require_all_fields,
                        help="Missing field: 'first_name'")
    parser.add_argument('last_name', type=str, required=require_all_fields,
                        help="Missing field: 'last_name'")
    parser.add_argument('email', type=str, required=require_all_fields,
                        help="Missing field: 'email'")
    parser.add_argument('password', type=str, required=require_all_fields,
                        help="Missing field: 'password'")
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

    def update_user(self, new_user: dict, user_id: int = None):
        """Update the given user.

        Args:
            new_user (dict): Updated user data.
            user_id (int): (Optional) ID of the user to update. If not provided, 
                           the user ID will be extrapolated from the user data.
        """
        match_id = user_id or new_user.get('id')
        if match_id is None:
            raise ValueError("No user ID provided and no ID could be extrapolated.")
        self.update(lambda user: user['id'] == match_id, new_user)

    def all_users(self) -> list:
        """Retrieve all user objects from the data source.

        Returns:
            (list) All users stored in the data source.
        """
        return self.read()


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
        user = _parse_user(require_all_fields=True)
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
        return  # TODO

    def put(self, user_id: int):
        """Update user with the given ID.

        Args:
            user_id (int): ID of the user to repace.
        """
        user = self.db.find_user_by_id(user_id)
        if not user:
            return '', 404
        query_params = _parse_user(require_all_fields=False)
        updated_user = {k: query_params.get(k) or user[k] for k in user}
        pass  # TODO

    def delete(self, user_id: int):
        """Delete user with the given ID.

        Args:
            user_id (int): ID of the user to delete.
        """
        pass  # TODO
