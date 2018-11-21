# pylint: disable=E1101
"""Class wrapping a user table."""
import re

from typing import TypeVar

from polyrides import db
from polyrides import models
from polyrides.exceptions import DuplicateEmailError
from polyrides.exceptions import InvalidEmailError
from polyrides.models import AbstractModelBase


UserType = TypeVar('UserType', bound='User')


class User(AbstractModelBase):
    """Data access object providing a static interface to a user table."""
    __tablename__ = models.tables.USER

    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))

    @db.validates('first_name')
    def validate_first_name(self, key: str, first_name: str):
        """Check that a first name is valid.

        Args:
            key (str): Dict key matching the validated field.
            first_name (str): Value provided to field.

        Raises:
            'InvalidFirstNameError': If the length of given first name is longer than 64
        """
        if len(first_name) > 64:
            raise InvalidFirstNameError(first_name)

        if re.compile('[~!@#$%^&*()+=_`]').search(first_name):
            raise InvalidFirstNameError(first_name)
        
        return first_name

    @db.validates('last_name')
    def validate_last_name(self, key: str, last_name: str):
        """Check that a first name is valid.

        Args:
            key (str): Dict key matching the validated field.
            last_name (str): Value provided to field.

        Raises:
            'InvalidLastNameError': If the length of given first name is longer than 64
        """
        if len(last_name) > 64:
            raise InvalidLastNameError(last_name)

        if re.compile('[~!@#$%^&*()+=_`]').search(last_name):
            raise InvalidLastNameError(last_name)

        return last_name

    @db.validates('email')
    def validate_email(self, key: str, email: str):
        """Check that an email is unique seems valid.

        Args:
            key (str): Dict key matching the validated field.
            email (str): Value provided to field.

        Return:
            str: Email if valid.

        Raises:
            `InvalidEmailError`: If the given email does not have exactly one '@' and a '.' after the '@'.
            `DuplicateEmailError`: If a user with the given email already exists.
        """

        """
        REGEX

        ^@ = any char except @
        \ = inhibit the specialness of character
        https://developers.google.com/edu/python/regular-expressions
        """

        if not re.compile(r'[^@]+@[^@]+\.[^@]+').match(email):
            raise InvalidEmailError(email)

        if self.find_by_email(email):
            raise DuplicateEmailError(email)

        return email

    def convert_name_to_lower(self, name: str):
        """Will be called after name is validated (no special char except '-').

        Args:
            name (str): name that will be converted into lower case.
        
        Return:
            str: name converted into lower case.

        """
        name = name.split("-")
        res = []

        for x in name:
            res.append(x.lower())

        joined = "-".join(res)

        return joined

    @staticmethod
    def find_by_id(user_id: int) -> UserType:
        """Look up a `User` by id.

        Args:
            id (int): id to match.

        Returns:
            User with the given id if found.
        """
        return db.session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def find_by_email(email: str) -> UserType:
        """Look up a `User` by email.

        Args:
            email (str): email to match.

        Returns:
            `User` with the given email if found.
        """
        return db.session.query(User).filter(User.email == email).first()