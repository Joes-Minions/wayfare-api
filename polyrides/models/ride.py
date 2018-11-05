# pylint: disable=E1101
"""Class wrapping a Ride table."""
from polyrides import db
# Included a table as an attribute in Rides 
# to support many-to-many relationships.
passengers = db.Table('passengers',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
        db.Column('ride_id', db.Integer, db.ForeignKey('rides.id'), primary_key=True)
        )


class Ride(db.Model):
    """Data access object providing a static interface to a Ride table."""
    __tablename__ = 'rides'
    # when creating fields to marshal in resource, only include 
    # Column Attributes
    # TODO : set up locations attribute
    # TODO : understand datetime attributes  

    # Column Attributes
    id = db.Column(db.Integer, primary_key=True)
    actual_leaving_time = db.Column(db.DateTime, 
                    nullable = True)  
    departure_date = db.Column(db.DateTime)
    ride_capacity = db.Column(db.Integer)
    time_range_id = db.Column(db.Integer,
                    db.ForeignKey('time_ranges.id'),
                    nullable=False) 
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    # Relationship Attributes
    time_range = db.relationship('TimeRange')
    driver = db.relationship('User', backref='drives', lazy=True)
    passengers = db.relationship('User', secondary=passengers, lazy='subquery',
        backref=db.backref('rides', lazy=True))

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
