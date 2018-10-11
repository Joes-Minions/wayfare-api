import json
import typing

from polyrides import util


class JsonWrapper(object):
    """A data access object providing an API for interacting with a JSON file."""
    def __init__(self, data_name: str, data_location: str = util.root_join('data'), indent: int = 4):
        """Initialize this wrapper with a file.

        Args:
            data_name (str): Name of the JSON data file.
            data_location (str): Path to directory containing JSON data.
            indent (int): Size of indent to use in JSON file.
        """
        self._data_file_path = util.root_join('data', data_name + '.json')
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

    def __repr__(self) -> str:
        return "JSON Wrapper for '{}'".format(self._data_file_path)