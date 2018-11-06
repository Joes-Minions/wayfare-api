# pylint: disable=E1101
"""Class wrapping a time range table."""
from typing import List

from polyrides import db

class TimeRange(db.Model):
    """Data access object providing a static interface to a user table."""
    __tablename__ = 'time_range'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    start_time = db.Column(db.Integer)
    end_time = db.Column(db.Integer)

    def create(self):
        """Add this `TimeRange` to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, new_fields: dict):
        """Update this `TimeRange`.

        Args:
            new_fields (dict): Dict containing new values for this `TimeRange`.
        """
        db.session.query(TimeRange).filter(TimeRange.id == self.id).update(new_fields)
        db.session.commit()

    def delete(self):
        """Delete this `TimeRange` from the database."""
        db.session.query(TimeRange).filter(TimeRange.id == self.id).delete()
        db.session.commit()

    @staticmethod
    def get_all() -> List['TimeRange']:
        """Return all `TimeRange`s in the database."""
        return db.session.query(TimeRange).all()

    @staticmethod
    def delete_all():
        """Delete all `TimeRange`s in the database."""
        db.session.query(TimeRange).delete()
        db.session.commit()

    # TODO: check this
    @staticmethod
    def find_by_id(time_range_id: int) -> 'Time Range':
        """Look up a `TimeRange` by id.

        Args:
            time_range_id (int): id to match.

        Returns:
            `TimeRange` with the given id if found.
        """
        return db.session.query(TimeRange).filter(TimeRange.id == time_range_id).first()

    @staticmethod
    def find_by_start_time(start_time: int) -> 'TimeRange':
        """Look up a `TimeRange` by start time.

        Args:
            start_time (int): start time to match.

        Returns:
            `TimeRange` with the given start time if found.
        """
        return db.session.query(TimeRange).filter(TimeRange.start_time == start_time).first()

    @staticmethod
    def find_by_end_time(end_time: int) -> 'TimeRange':
        """Look up a `Time Range` by end time.

        Args:
            end_time (int): end time to match.

        Returns:
            `TimeRange` with the given end time if found.
        """
        return db.session.query(TimeRange).filter(TimeRange.end_time == end_time).first()
