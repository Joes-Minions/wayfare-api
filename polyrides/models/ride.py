# pylint: disable=E1101
"""Class wrapping a Ride table."""
from typing import List

from polyrides import db
from polyrides import models

from polyrides.models.location import Location
from polyrides.models.time_range import TimeRange
from polyrides.models.user import User


# quan: hmm...
# Included a table as an attribute in Rides to support many-to-many relationships.
_PASSENGERS = db.Table(
    'passengers',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey(models.tables.USER + '.id'),
              primary_key=True),
    db.Column('ride_id',
              db.Integer,
              db.ForeignKey(models.tables.RIDE + '.id'),
              primary_key=True)
)


class Ride(db.Model):
    """Data access object providing a static interface to a Ride table."""
    __tablename__ = models.tables.RIDE

    # when creating fields to marshal in resource, only include ??
    # TODO : understand datetime attributes

    # Column Attributes
    id = db.Column(db.Integer, primary_key=True)
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
    passengers = db.relationship(User,
                                 secondary=_PASSENGERS,
                                 backref=db.backref('rides', lazy=True))
    start_location = db.relationship(Location, foreign_keys=[start_location_id])
    destination = db.relationship(Location, foreign_keys=[destination_id])

    def create(self):
        """Add this `Ride` to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, new_fields: dict):
        """Update this `Ride`.

        Args:
            new_fields (dict): Dict containing new values for this `Ride`.
        """
        db.session.query(Ride).filter(Ride.id == self.id).update(new_fields)
        db.session.commit()

    def delete(self):
        """Delete this `Ride` from the database."""
        db.session.query(Ride).filter(Ride.id == self.id).delete()
        db.session.commit()

    @staticmethod
    def get_all() -> List['Ride']:
        """Return all `Ride`s in the database."""
        return db.session.query(Ride).all()

    @staticmethod
    def delete_all():
        """Return all `Ride`s in the database."""
        db.session.query(Ride).delete()
        db.session.commit()

    @staticmethod
    def find_by_id(ride_id: int) -> 'Ride':
        """Look up a `Ride` by id.

        Args:
            id (int): id to match.

        Returns:
            Ride with the given id if found.
        """
        return db.session.query(Ride).filter(Ride.id == ride_id).first()
