"""Exceptions raised by PolyRides API routes and models."""

class DuplicateEmail(Exception):
    """Exception indicating that a `User` email already exists.

    Attributes:
        email (str): Duplicate email that raised this exception.
    """
    def __init__(self, email: str):
        """Init DuplicateEmail with the given email."""
        self.email = email
        self.message = "Duplicate email: '{}'".format(email)
        super().__init__(self.message)
