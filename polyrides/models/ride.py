# pylint: disable=E1101
"""Class wrapping a Ride table."""
from typing import TypeVar

from polyrides import db
from polyrides import models

from polyrides.models import AbstractModelBase
from polyrides.models import Location
from polyrides.models import TimeRange
from polyrides.models import User
from polyrides.models.passenger import Passenger


RideType = TypeVar('RideType', bound='Ride')


class Ride(AbstractModelBase):
    """Data access object providing a static interface to a Ride table."""
    __tablename__ = models.tables.RIDE

    # Column Attributes
    actual_departure_time = db.Column(db.DateTime)
    departure_date = db.Column(db.Date)
    capacity = db.Column(db.Integer)
    time_range_id = db.Column(db.Integer,
                              db.ForeignKey(models.tables.TIME_RANGE + '.id'),
                              nullable=False)
    driver_id = db.Column(db.Integer,
                          db.ForeignKey(models.tables.USER + '.id'),
                          nullable=False)
    start_location_id = db.Column(db.Integer,
                                  db.ForeignKey(models.tables.LOCATION + '.id'),
                                  nullable=False)
    destination_id = db.Column(db.Integer,
                               db.ForeignKey(models.tables.LOCATION + '.id'),
                               nullable=False)

    # Relationship Attributes
    time_range = db.relationship(TimeRange)
    # TODO : Figure out this backref thing
    driver = db.relationship(User, backref='drives', lazy=True)
    passengers = db.relationship(Passenger, cascade="all, delete-orphan")
    start_location = db.relationship(Location, foreign_keys=[start_location_id])
    destination = db.relationship(Location, foreign_keys=[destination_id])

    @staticmethod
    def find_by_id(ride_id: int) -> RideType:
        """Look up a `Ride` by id.

        Args:
            id (int): id to match.

        Returns:
            Ride with the given id if found.
        """
        return db.session.query(Ride).filter(Ride.id == ride_id).first()
