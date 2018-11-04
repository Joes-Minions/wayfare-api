"""Flask-RESTful resources for interacting with user data."""
# pylint: disable=E1101

import flask_restful

from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from polyrides import db
from polyrides.models.user import User


_USER_FIELDS = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password': fields.String
}


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
    """Resource for interacting with general user data."""
    @marshal_with(_USER_FIELDS)
    def get(self):
        """Get all users."""
        users = db.session.query(User).all()
        return users

    # @marshal_with(_USER_FIELDS)
    def post(self):
        """Add a user."""
        parsed_user = _parse_user_from_request_body(require_all_fields=True)
        user_with_email = db.session.query(User).filter(User.email == parsed_user.email).first()
        if user_with_email:
            abort(400, message="Duplicate email: '{}'".format(parsed_user.email))
        user = User(**parsed_user)
        db.session.add(user)
        db.session.commit()
        return '', 201

    def delete(self):
        """Delete all users."""
        db.session.query(User).delete()
        db.session.commit()
        return '', 200


class UserById(flask_restful.Resource):
    """Resource for interacting with user data based on a user id."""
    @marshal_with(_USER_FIELDS)
    def get(self, user_id):
        """Get a user resource by id.

        Args:
            user_id (int): id of the user to look up.

        Returns:
            User with the given id if found.
        """
        user = db.session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message="User {} does not exist".format(user_id))
        return user

    def put(self, user_id):
        """Create or update a user resource by id.

        Args:
            user_id (int): id of the user to create or update.

        Returns:
            Updated User.
        """
        parsed_user = _parse_user_from_request_body(require_all_fields=True)
        user = db.session.query(User).filter(User.id == user_id).first()
        if user:
            db.session.query(User).filter(User.id == user_id).update(parsed_user)
            db.session.commit()
            return user, 200
        else:
            user = User(**parsed_user)
            db.session.add(user)
            db.session.commit()
            return user, 201

    def delete(self, user_id):
        """Delete user with the given id.

        Args:
            user_id (int): id of the user to delete
        """
        user = db.session.query(User).filter(User.id == user_id).first()
        if user:
            db.session.query(User).filter(User.id == user_id).delete()
            db.session.commit()
            return '', 200
        else:
            return '', 404
            # abort(404, message="User {} does not exist".format(user_id))
