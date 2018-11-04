"""Flask-SQLAlchemy model representing a User object.

Provides convenience methods for performing database transactions.
"""
from polyrides import db


class User(db.Model):
    """Model representing a user."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))

    # def __init__(self, first_name=None, last_name=None, email=None, password=None):
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email
    #     self.password = password

    def create(self):
        """Add this User to the database.
        TODO: Maybe move all User creation functionality here."""
        pass

    @staticmethod
    def find_by_id(user_id: int):
        """Look up a user by id.

        Args:
            id (int): user id to search for.

        Returns:
            User with the given id if found.
        """
        return db.session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def find_by_email(email: str):
        """Look up a user by email.

        Args:
            email (str): user email to search for.

        Returns:
            User with the given email if found.
        """
        return db.session.query(User).filter(User.email == email).first()
