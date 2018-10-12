"""This is the main driver and entrypoint for the polyrides API.

Sets up and runs our Flask app.
"""
import argparse

from flask import Flask, jsonify
from flask_restful import Api, Resource

from polyrides.routes import test
from polyrides.routes import users


class Index(Resource):
    """An example Resource to be attached to the root ('/') endpoint of our Flask app.

    All it does is return a message in response to an HTTP GET request.
    """
    def __init__(self):
        """Initialize the Resource, setting the default message.

        This method is called every time the endpoint receives a request.
        """
        print('Called Index.__init__.')
        self._msg = "Hello World!"

    def get(self):
        """Respond to a get request on this endpoint, returning this resource's message as JSON."""
        return jsonify(self._msg)


def _parse_args() -> argparse.Namespace:
    """... Parse arguments."""
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--debug',
                        help="Start the app in debug mode.",
                        action='store_true',
                        default=False)
    parser.add_argument('--example_value',
                        help="Pass an example value to this application. It doesn't do anything, but this illustrates how arguments are accessed.")
    return parser.parse_args()


def main():
    """This is the main function. It runs the Flask app."""

    # Parse the arguments passed to the command running this application.
    args = _parse_args()

    # This is how arguments are retrieved from the Namespace object returned by parse_args.
    if args.example_value is not None:
        my_value = args.example_value
        print('You passed `{}` as the example value!'.format(my_value))

    # Construct an instance of a Flask app. This app will have all of the functionality provided by Flask.
    app = Flask(__name__)

    # This configures the app's `debug` mode, which is an option provided as a command line argument.
    # Debug mode will re-load the server when it detects a change in the source files and will give
    # helpful messages when something breaks.
    # Of course, we don't want these messages to appear in production since it will reveal details
    # about how our code works to end users.
    app_args = {
        'debug': args.debug,
        'port': 5000
    }

    # These are keyword args passed to the flask_restful.Api constructor.
    # In this case, it just tells the app to handle all 404 errors for us.
    api_args = {
        'catch_all_404s': True
    }

    # Construct the REST API object attached to our Flask app defined above.
    api = Api(app, **api_args)

    # Set the Index resource we defined above as the handler for requests to the {base_url}.
    api.add_resource(Index, '/')
    # Set the Test resource defined in routes/test.py as the handler for all requests to {base_url}/test.
    api.add_resource(test.Test, '/test')
    # Do the same for the Users resource. This is another way to reference a module in routes.
    api.add_resource(users.Users, '/users')
    api.add_resource(users.UserById, '/users/<int:user_id>')
    # When a new resource is created, it must be added here so that our app knows about it.

    # With setup complete, run the application.
    app.run(**app_args)


if __name__ == '__main__':
    main()
