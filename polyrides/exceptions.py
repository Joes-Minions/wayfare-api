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


class MissingField(Exception):
    """Exception raised when a request body is missing a required field.

    Attributes:
        field (str): Name of missing field.
    """
    def __init__(self, field: str):
        """Init MissingField with the given field_name."""
        self.field = field
        self.message = "Missing field: '{}'".format(field)
        super().__init__(self.message)
