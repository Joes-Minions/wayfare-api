# pylint: disable=E1101
"""Class wrapping a Ride table."""
from polyrides import db


class Ride(db.Model):
    """Data access object providing a static interface to a Ride table."""
    __tablename__ = 'Rides'

    id = db.Column(db.Integer, primary_key=True)
    # first_name = db.Column(db.String(64))
    # last_name = db.Column(db.String(64))
    # email = db.Column(db.String(64))
    # password = db.Column(db.String(64))

    def create(self):
        """Add this `Ride` to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, new_fields: dict):
        """Update this `Ride`.

        Args:
            new_fields (dict): Dict containing new values for this `Ride`.
        """


    def delete(self):
        """Delete this `Ride` from the database."""
        db.session.query(Ride).filter(Ride.id == self.id).delete()
        db.session.commit()

    @staticmethod
    def get_all():
        """Return all `Ride`s in the database."""
        return db.session.query(Ride).all()

    @staticmethod
    def delete_all():
        """Return all `Ride`s in the database."""
        db.session.query(Ride).delete()
        db.session.commit()

    @staticmethod
    def find_by_id(ride_id: int) -> 'Ride':
        """Look up a `Ride`s by id.

        Args:
            id (int): id to match.

        Returns:
            Ride with the given id if found.
        """
        return db.session.query(Ride).filter(Ride.id == ride_id).first()