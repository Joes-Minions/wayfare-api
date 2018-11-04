"""Flask-RESTful resources for interacting with ride data."""
import flask
import flask_restful

from flask_restful import abort
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from polyrides.models.ride import Ride


_BASE_URL = 'rides' 
_RIDE_FIELDS = {
}