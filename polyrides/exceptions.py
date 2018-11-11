"""Exceptions raised by PolyRides API routes and models."""


class PolyRidesError(Exception):
    """Base Exception class for all user-defined errors."""
    pass


class DuplicateEmailError(PolyRidesError):
    """Exception indicating that a `User` email already exists.

    Attributes:
        email (str): Duplicate email that raised this exception.
    """
    def __init__(self, email: str):
        """Init `DuplicateEmailError` with the given email."""
        self.email = email
        self.message = "Duplicate email: '{}'".format(email)
        super().__init__(self.message)


class InvalidEmailError(PolyRidesError):
    """Exception raised when a provided email value is invalid. 

    Attributes:
        email (str): Invalid email that raised this exception.
    """
    def __init__(self, email: str):
        """Init `DuplicateEmailError` with the given email."""
        self.email = email
        self.message = "Invalid email: '{}'".format(email)
        super().__init__(self.message)
