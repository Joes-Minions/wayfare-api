"""Contains classes for accessing JSON data.

Defines a base JsonWrapper and Data Access Object subclasses that work with specific types of data.
"""
import json
import os
import typing

from polyrides import util


class JsonWrapper(object):
    """A data access object providing an API for interacting with a JSON file.
    
    This class should not be used directly. Subclass it instead."""
    def __init__(self, data_name: str, data_location: str = util.root_join('data', 'json'), indent: int = 4):
        """Initialize this wrapper with a file.

        Args:
            data_name (str): Name of the JSON data file.
            data_location (str): Path to directory containing JSON data.
            indent (int): Size of indent to use in JSON file.
        """
        self._data_file_path = os.path.join(data_location, data_name + '.json')
        self._indent = indent

    def read(self) -> list:
        """Read all items from the JSON file.

        Returns:
            (list): A list of all items contained in the file.
        """
        with open(self._data_file_path) as data_fp:
            all_data = json.load(data_fp)
        return all_data

    def write(self, items: list):
        """Write the given items to the JSON file. Overwrites the file.

        Args:
            items (list): The items to write to the file.
        """
        with open(self._data_file_path, 'w') as data_fp:
            data_fp.write(json.dumps(items, indent=self._indent))

    def create(self, item: dict):
        """Add an item to the JSON file.

        Args:
            item (dict): The item to add.
        """
        all_items = self.read()
        all_items.append(item)
        self.write(all_items)

    def find(self, predicate: typing.Callable[[dict], bool]) -> dict:
        """Find the first item that passes the provided predicate.

        Args:
            predicate (function): Function that takes a dict and returns a boolean.

        Returns:
            (dict): The first item that passes the predicate.
        """
        for item in self.read():
            if predicate(item):
                return item

    def find_all(self, predicate: typing.Callable[[dict], bool]) -> dict:
        """Find all items that pass the provided predicate.

        Args:
            predicate (function): Function that takes a dict and returns a boolean.

        Yields:
            (dict): The next item that passes the predicate.
        """
        for item in self.read():
            if predicate(item):
                yield item

    def delete(self, predicate: typing.Callable[[dict], bool]) -> bool:
        """Delete all items that pass the provided predicate.

        Args:
            predicate (function): Function that takes a dict and returns a boolean.

        Returns:
            (bool): True if an item was deleted. False otherwise.
        """
        all_items = self.read()
        new_items = [item for item in all_items if not predicate(item)]
        self.write(new_items)
        return len(all_items) != len(new_items)

    def update(self, predicate: typing.Callable[[dict], bool], updated_item: dict) -> bool:
        """Update all items that pass the provided predicate with the given item.

        Args:
            predicate (function): Function that takes a dict and returns a boolean.
            updated_item (dict): Item to replace the each item that passes the predicate.

        Returns:
            (bool): True if an item was replaced. False otherwise.
        """
        all_items = self.read()
        new_items = [updated_item if predicate(item) else item for item in all_items]
        self.write(new_items)
        return all_items != new_items

    def nuke(self):
        """Delete all items."""
        self.write([])

    def __repr__(self) -> str:
        return "JSON Wrapper for '{}'".format(self._data_file_path)

from polyrides.data.json_wrapper import JsonWrapper


class UserDAO(JsonWrapper):
    """Data Access Object that provides methods for interacting with user data."""

    def __init__(self):
        super().__init__('users')

    def create_user(self, user: dict):
        """Add a user to the data source, generating an id for the user.

        Args:
            user (dict): A dictionary representation of a user.
        """
        if not self.all_users():  # Set the first user's ID to 1.
            new_user_id = 1
        else:                     # This will reuse an ID if the most recently added user is deleted, but who cares?
            all_user_ids = [user['id'] for user in self.all_users()]
            max_id = max(all_user_ids)
            new_user_id = max_id + 1
        user['id'] = new_user_id
        self.create(user)

    def find_user_by_id(self, user_id: int) -> dict:
        """Search the data source for a user with the given id.
        Returns None if no matches are found.
        
        Args:
            user_id (int): User ID to look up.
        
        Returns:
            (dict) User with the given ID if found.
        """
        return self.find(lambda user: user['id'] == user_id)

    def find_user_by_email(self, email: str) -> dict:
        """Search the data source for a user with the given email.
        Returns None if no matches are found.
        
        Args:
            email (str): User email address to look up.
        
        Returns:
            (dict) User with the given email if found.
        """
        return self.find(lambda user: user['email'] == email)

    def find_users_with_first_name(self, name: str) -> list:
        """Search the data source for all users with the given first name.
        Returns an empty list if no matches are found.
        
        Args:
            name (str): First name to search for.
        
        Returns:
            (list) List of all users with the given first name.
        """
        return self.find(lambda user: user['first_name'] == name)

    def find_users_with_last_name(self, name: str) -> list:
        """Search the data source for all users with the given last name.
        Returns an empty list if no matches are found.
        
        Args:
            name (str): Last name to search for.
        
        Returns:
            (list) List of all users with the given last name.
        """
        return self.find(lambda user: user['last_name'] == name)

    def update_user(self, new_user: dict, user_id: int = None):
        """Update the given user.

        Args:
            new_user (dict): Updated user data.
            user_id (int): (Optional) ID of the user to update. If not provided, 
                           the user ID will be extrapolated from the user data.
        """
        match_id = user_id or new_user.get('id')
        if match_id is None:
            raise ValueError("No user ID provided and no ID could be extrapolated.")
        self.update(lambda user: user['id'] == match_id, new_user)

    def all_users(self) -> list:
        """Retrieve all user objects from the data source.

        Returns:
            (list) All users stored in the data source.
        """
        return self.read()

    def del_user_by_id(self, user_id: int):
        """Delete the given user.

        Args:
            user_id (int): user_id of user to be deleted
        """
        self.delete(lambda user: user['id'] == user_id)
