"""The main driver and entrypoint for the Polyrides API."""

import argparse
import flask_restful
import flask_sqlalchemy

from flask import Flask


DB_URI = 'sqlite:///./main.db'


app = Flask(__name__)  # pylint: disable=C0103
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

db = flask_sqlalchemy.SQLAlchemy(app)  # pylint: disable=C0103
<<<<<<< HEAD
from polyrides.models import Location  # pylint: disable=C0413
from polyrides.models import Status  # pylint: disable=C0413
from polyrides.models import TimeRange  # pylint: disable=C0413
from polyrides.models import User  # pylint: disable=C0413
from polyrides.models import Ride  # pylint: disable=C0413
from polyrides.models import Passenger  # pylint: disable=C0413
=======
from polyrides.models.location import Location  # pylint: disable=C0413
from polyrides.models.ride import Ride  # pylint: disable=C0413
from polyrides.models.time_range import TimeRange  # pylint: disable=C0413
from polyrides.models.user import User  # pylint: disable=C0413
from polyrides.models.passenger import Passenger  # pylint: disable=C0413

>>>>>>> removed passengers table, created a new model (Passenger) for creating instances of passengers
# Necessary for sqlite
db.drop_all()
db.create_all()

api = flask_restful.Api(app, catch_all_404s=True)  # pylint: disable=C0103
