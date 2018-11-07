# pylint: disable=E1101
"""Class wrapping a Passenger table."""
from typing import List

from polyrides import db
from polyrides import models


class Passenger(db.Model):
    """Data access object providing a static interface to a Passenger table."""
    __tablename__ = models.tables.PASSENGER
    # Column Attributes
    user_id = db.Column(db.Integer,
                        db.ForeignKey(models.tables.USER + '.id', ondelete='CASCADE'),
                        primary_key=True)
    ride_id = db.Column(db.Integer,
                        db.ForeignKey(models.tables.RIDE + '.id', ondelete='CASCADE'),
                        primary_key=True)
    status_id = db.Column(db.Integer,
                        db.ForeignKey(models.tables.STATUS + '.id'),
                        primary_key=True)
    # Relationship Attributes
    db.UniqueConstraint('user_id', 'ride_id', 'status_id')
    db.relationship('User', 
                    uselist=False,
                    backref=db.backref('passenger', passive_deletes=True),
                    lazy='dynamic', 
                    passive_deletes=True)
    db.relationship('Ride', 
                    uselist=False, 
                    backref=db.backref('passenger', passive_deletes=True),
                    lazy='dynamic', 
                    passive_deletes=True)
    db.relationship('Status', 
                    uselist=False, 
                    lazy='dynamic')
    
    def create(self):
        """Add this `Passenger` to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, new_fields: dict):
        """Update this `Passenger`.

        Args:
            new_fields (dict): Dict containing new values for this `Passenger`.
        """
        db.session.query(Passenger).filter(Passenger.user_id == self.user_id).update(new_fields)
        db.session.commit()

    def delete(self):
        """Delete this `Passenger` from the database."""
        db.session.query(Passenger).filter(Passenger.user_id == self.user_id).delete()
        db.session.commit()

    @staticmethod
    def get_all() -> List['Passenger']:
        """Return all `Passenger`s in the database."""
        return db.session.query(Passenger).all()

    @staticmethod
    def delete_all():
        """Delete all `Passenger`s in the database."""
        db.session.query(Passenger).delete()
        db.session.commit()

    @staticmethod
    def find_by_ride_id(ride_id: int) -> List['Passenger']:
        """Look up a `Passenger` by ride_id.

        Args:
            ride_id (int): id to match.

        Returns:
            `Passenger`s associated with the given ride_id if found.
        """
        return db.session.query(Passenger).filter(Passenger.ride_id == ride_id)
    
    @staticmethod
    def find_by_user_id(user_id: int) -> List['Passenger']:
        """Look up a `Passenger` by user_id.

        Args:
            ride_id (int): id to match.

        Returns:
            `Passenger`s associated with the given user_id if found.
        """
        return db.session.query(Passenger).filter(Passenger.user_id == user_id)

    @staticmethod
    def find_by_status_id(status_id: int) -> List['Passenger']:
        """Look up a `Passenger` by status_id.

        Args:
            status_id (int): id to match.

        Returns:
            `Passenger`s associated with the given status_id if found.
        """
        return db.session.query(Passenger).filter(Passenger.status_id == status_id)

