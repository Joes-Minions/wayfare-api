# pylint: disable=E1101
"""Class wrapping a Ride table."""
from polyrides import db


class Ride(db.Model):
    """Data access object providing a static interface to a Ride table."""
    __tablename__ = 'rides'

    id = db.Column(db.Integer, primary_key=True)
    start_location = db.Column(db.String(64))
    end_location = db.Column(db.String(64))
    departure_date = db.Column(db.String(64))
    # time_range_id = db.Column(db.Integer,
    #                 db.ForeignKey('timerange.id'),
    #                 nullable=False) 
    # todo : relationally maps to time_range id to model of time_range
    ride_capacity = db.Column(db.Integer)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)

    driver = db.relationship('User', backref='drives', lazy=True)
    # actual_leaving_time = db.Column(db.DateTime, 
    #                         nullable = True)  
    # todo : figure out how to set up datetime attributes  
    def create(self):
        """Add this `Ride` to the database."""
        db.session.add(self)
        db.session.commit()

    def update(self, new_fields: dict):
        """Update this `Ride`.

        Args:
            new_fields (dict): Dict containing new values for this `Ride`.
        """
        db.session.query(Ride).filter(Ride.id == self.id).update(new_fields)
        db.session.commit()

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
