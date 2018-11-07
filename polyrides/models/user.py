# pylint: disable=E1101
"""Class wrapping a user table."""
from typing import List

from polyrides import db
from polyrides import models


class User(db.Model):
    """Data access object providing a static interface to a user table."""
    __tablename__ = models.tables.USER

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def create(self):
        """Add this `User` to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, new_fields: dict):
        """Update this `User`.

        Args:
            new_fields (dict): Dict containing new values for this `User`.
        """
        user = db.session.query(User).filter(User.id == self.id).first()
        db.session.commit()

    def delete(self):
        """Delete this `User` from the database."""
        db.session.query(User).filter(User.id == self.id).delete()
        db.session.commit()

    @staticmethod
    def get_all() -> List['User']:
        """Return all `User`s in the database."""
        return db.session.query(User).all()

    @staticmethod
    def delete_all():
        """Return all `User`s in the database."""
        db.session.query(User).delete()
        db.session.commit()

    @staticmethod
    def find_by_id(user_id: int) -> 'User':
        """Look up a `User` by id.

        Args:
            id (int): id to match.

        Returns:
            User with the given id if found.
        """
        return db.session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def find_by_email(email: str) -> 'User':
        """Look up a `User` by email.

        Args:
            email (str): email to match.

        Returns:
            `User` with the given email if found.
        """
        return db.session.query(User).filter(User.email == email).first()
