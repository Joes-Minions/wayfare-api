"""Endpoint for retrieving test data.

This class is a Resource mounted at {base_url}/test in our app's main function.
"""
import json

from typing import Dict, List

from flask import jsonify
from flask_restful import reqparse, Resource

from polyrides import util


def _parse_request() -> Dict:
    """Parse the JSON body of an HTTP POST request.

    When this function is called, it parses a global (but local to the context) variable called
    `request`. Performing the parsing in this function keeps the code from being cluttered by
    references to a `request` variable.

    Returns:
        Data from a request parsed according to the arguments defined in this function.
        For example, a dict of the following format would be returned (unless this function has
        changed since I wrote it.)
        {
            'id': 1,
            'msg': 'Oliver likes cats'
        }
    """
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int, help="A unique integer ID.")
    parser.add_argument('msg', type=str, help="A string message.")
    # parser.add_argumemt('name_of_field', type=str, help="This is how you would add another argument.")
    return parser.parse_args()


class Test(Resource):
    """Flask RESTful resource for interacting with test data.

    This class extends the flash_restful.Resource class and is instantiated in app.py in the root
    directory. This should be the exclusive point of entry for all functionality provided by the
    {base_url}/test/ endpoint.
    """

    def __init__(self):
        """Initialize the Resource, loading data from the source (which in this case is a JSON file).

        This method is called every time the endpoint receives a request.
        """
        print('Called Test.__init__.')
        self._data_file = util.root_join('data', 'json/test.json')
        self.data = util.load_json(self._data_file)

    def _write(self, data: List):
        """Serialize data, persisting it to some permanent storage medium.

        In this example, we are serializing data locally in a JSON file. This is a bad idea. IRL,
        we would use a database connection. Maybe SQL, maybe not. But probably SQL.
        We are only doing this serialization to JSON thing to illustrate the idea of saving data
        and mostly because it doesn't require any setup.

        Args:
            data (list): The list of test items we are writing to disk.
        """
        with open(self._data_file, 'w') as t_f:
            t_f.write(json.dumps(data, indent=4))

    def get(self):
        """A GET request retrieves a document from the API.

        In this case, a GET request to the base of this endpoint will retrieve all items tracked
        by this resource.
        """
        return jsonify(self.data)  # By default, return HTTP Status 200, indicating 'OK'

    def post(self):
        """A POST request to the API creates a document.

        This endpoint expects the request to contain an object to add to Test collection.
        """
        item = _parse_request()
        # If the item matches the expected format, add it to the collection and save it.
        # In an actual situation you would want to create and raise custom Exceptions to provide
        # more data/context, but this is just an example so chill, damn.
        try:
            item_id = item['id']

            if not item_id:
                raise Exception('Bad Request: empty ID.')
            if not item['msg']:
                raise Exception('Bad Request: empty message.')
            # Check if the item ID is not unique.
            if item_id in (saved_item['id'] for saved_item in self.data):
                raise Exception('Bad Request: duplicate ID.')

            # Add the item to the data and sort by ID if the item is valid,
            updated_data = sorted(self.data + [item], key=lambda item: item['id'])
            self._write(updated_data)
            return jsonify(''), 201  # Return an empty response with HTTP Status 201, indicating 'Created'
        except Exception as err:
            # Return HTTP Status 400, indicating 'Bad Request'
            return str(err), 400
