"""Unit tests for User models."""
import unittest

from polyrides.exceptions import DuplicateEmailError
from polyrides.exceptions import InvalidEmailError
from polyrides.models import User

class TestValidation(unittest.TestCase):
    """Tests for the User model."""
    def setUp(self):
        User.delete_all()

    def test_invalid_email(self):
        invalid_email = 'not_an_email'
        with self.assertRaises(InvalidEmailError):
            User(
                first_name='Tony',
                last_name='Stark',
                email=invalid_email,
                password='password123'
            )

    def test_duplicate_email(self):
        duplicate_email = 'email@example.com'
        user_with_email = User(
            first_name='test',
            last_name='test',
            email=duplicate_email,
            password='test'
        )
        user_with_email.create()
        with self.assertRaises(DuplicateEmailError):
            User(
                first_name='Tony',
                last_name='Stark',
                email=duplicate_email,
                password='password123'
            )


if __name__ == '__main__':
    unittest.main()
