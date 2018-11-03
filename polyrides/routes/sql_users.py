"""Flask-RESTful resources for interacting with user data."""

import flask
import flask_restful

from polyrides.data.db import session
from polyrides.data.models import User

from flask import jsonify
from flask_restful import reqparse
from flask_restful import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with

# set up the field filtering for data objects from the API
user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str)
parser.add_argument('last_name', type=str)

# marshall_with decorator takes data objects 
# from API and applies field filtering.

class Users(Resource):
    """Resource for interacting with all user data."""
    @marshal_with(user_fields)
    def get(self):
        """Get a user resource."""
        users = session.query(User).all()
        return users

    @marshal_with(user_fields)
    def post(self):
        """Add a user resource."""
        parsed_args = parser.parse_args()
        user = User(first_name=parsed_args['first_name'],last_name=parsed_args['last_name'])
        session.add(user)
        session.commit()
        return user, 201


class UserById(Resource):
    """Resource for interacting with database using user ID."""
    @marshal_with(user_fields)
    def get(self, user_id):
        """Get a user resource by ID"""
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(user_id))
        return user