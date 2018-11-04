"""The main driver and entrypoint for the Polyrides API."""

import argparse
import flask_restful
import flask_sqlalchemy

from flask import Flask

from polyrides.routes import users


def _parse_args() -> argparse.Namespace:
    """... Parse arguments."""
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--debug',
                        help="Start the app in debug mode.",
                        action='store_true',
                        default=False)
    parser.add_argument('--port',
                        help="The port to listen on.",
                        type=int,
                        default=5000)
    return parser.parse_args()


app = Flask(__name__)
api = flask_restful.Api(app, catch_all_404s=True)


if __name__ == '__main__':
    """Set up and run the Flask app."""
    args = _parse_args()

    api.add_resource(users.Users, '/users', endpoint='users')

    app.debug = args.debug
    app.run(port=args.port)
