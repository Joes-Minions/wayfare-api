# pylint: disable=E1101
"""Class wrapping a status table."""
from typing import List

from polyrides import db
from polyrides import models

class Status(db.Model):
    """Data access object providing a static interface to a status table."""
    __tablename__ = models.tables.STATUS

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))

    def create(self):
        """Add this `Status` to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, new_fields: dict):
        """Update this `Status`.

        Args:
            new_fields (dict): Dict containing new values for this `Status`.
        """
        db.session.query(Status).filter(Status.id == self.id).update(new_fields)
        db.session.commit()

    def delete(self):
        """Delete this `Status` from the database."""
        db.session.query(Status).filter(Status.id == self.id).delete()
        db.session.commit()

    @staticmethod
    def get_all() -> List['Status']:
        """Return all `Status`s in the database."""
        return db.session.query(Status).all()

    @staticmethod
    def delete_all():
        """Delete all `Status` in the database."""
        db.session.query(Status).delete()
        db.session.commit()

    @staticmethod
    def find_by_id(status_id: int) -> 'Status':
        """Look up a `Status` by id.

        Args:
            status_id (int): id to match.

        Returns:
            `Status` with the given id if found.
        """
        return db.session.query(Status).filter(Status.id == status_id).first()

    @staticmethod
    def find_by_description(description: str) -> 'Status':
        """Look up a `Status` by descripttion.

        Args:
            description: (str): description to match.

        Returns:
            `Status` with the given description if found.
        """
        return db.session.query(Status).filter(Status.description == description).first()
