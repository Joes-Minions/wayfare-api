# pylint: disable=E1101
"""Class wrapping a time range table."""
from polyrides import db

class TimeRange(db.Model):
    """Data access object providing a static interface to a user table."""
    __tablename__ = 'time_ranges'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    start_time = db.Column(db.Integer))
    end_time = db.Column(db.Integer))

    def create(self):
        """Add this `Time Range` to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, new_fields: dict):
        """Update this `Time Range`.

        Args:
            new_fields (dict): Dict containing new values for this `Time Range`.
        """
        db.session.query(TimeRange).filter(TimeRange.id == self.id).update(new_fields)
        db.session.commit()

    def delete(self):
        """Delete this `Time Range` from the database."""
        db.session.query(TimeRange).filter(TimeRange.id == self.id).delete()
        db.session.commit()

    @staticmethod
    def get_all():
        """Return all `Time Range`s in the database."""
        return db.session.query(TimeRange).all()

    @staticmethod
    def delete_all():
        """Delete all `Time Range`s in the database."""
        db.session.query(TimeRange).delete()
        db.session.commit()

## check this
    @staticmethod
    def find_by_id(timerange_id: int) -> 'Time Range':
        """Look up a `Time Range` by id.

        Args:
            id (int): id to match.

        Returns:
            Time Range with the given id if found.
        """
        return db.session.query(TimeRange).filter(TimeRange.id == timerange_id).first()

    @staticmethod
    def find_by_start_time(start_time: int) -> 'Time Range': 
        """Look up a `Time Range` by start time.

        Args:
            start_time (int): start_time to match.

        Returns:
            `Time Range` with the given start time if found.
        """
        return db.session.query(TimeRange).filter(TimeRange.start_time == start_time).first()

    @staticmethod
    def find_by_end_time(end_time: int) -> 'Time Range':
        """Look up a `Time Range` by end time.

        Args:
            end_time (int): end_time to match.

        Returns:
            `Time Range` with the given end time if found.
        """
        return db.session.query(TimeRange).filter(TimeRange.end_time == end_time).first()
