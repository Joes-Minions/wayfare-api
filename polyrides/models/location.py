# pylint: disable=E1101
"""Class wrapping a location table."""
from typing import List

from polyrides import db


class Location(db.Model):
    """Data access object providing a static interface to a location table."""
    __tablename__ = 'location'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    def create(self):
        """Add this `Location` to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, new_fields: dict):
        """Update this `Location`.

        Args:
            new_fields (dict): Dict containing new values for this `Location`.
        """
        db.session.query(Location).filter(Location.id == self.id).update(new_fields)
        db.session.commit()

    def delete(self):
        """Delete this `Location` from the database."""
        db.session.query(Location).filter(Location.id == self.id).delete()
        db.session.commit()

    @staticmethod
    def get_all() -> List['Location']:
        """Return all `Location`s in the database."""
        return db.session.query(Location).all()

    @staticmethod
    def delete_all():
        """Delete all `Location`s in the database."""
        db.session.query(Location).delete()
        db.session.commit()

    @staticmethod
    def find_by_id(location_id: int) -> 'Location':
        """Look up a `Location` by id.

        Args:
            location_id (int): id to match.

        Returns:
            `Location` with the given id if found.
        """
        return db.session.query(Location).filter(Location.id == location_id).first()

    @staticmethod
    def find_by_name(name: str) -> 'Location':
        """Look up a `Location` by name.

        Args:
            name (str): name to match.

        Returns:
            `Location` with the given name if found.
        """
        return db.session.query(Location).filter(Location.name == name).first()
