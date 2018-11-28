# pylint: disable=E1101
"""Class wrapping a status table."""
from typing import TypeVar

from polyrides import db
from polyrides import models

from polyrides.models import AbstractModelBase


StatusType = TypeVar('StatusType', bound='Status')


class Status(AbstractModelBase):
    """Data access object providing a static interface to a status table."""
    __tablename__ = models.tables.STATUS

    description = db.Column(db.String(64))

    @staticmethod
    def find_by_id(status_id: int) -> StatusType:
        """Look up a `Status` by id.

        Args:
            status_id (int): id to match.

        Returns:
            `Status` with the given id if found, None if not found.
        """
        return db.session.query(Status).get(status_id)

    @staticmethod
    def find_by_description(description: str) -> StatusType:
        """Look up a `Status` by descripttion.

        Args:
            description: (str): description to match.

        Returns:
            `Status` with the given description if found, None if not found.
        """
        return db.session.query(Status).filter(Status.description == description).first()
