"""The main driver and entrypoint for the Polyrides API."""
import argparse

from polyrides import app
from polyrides import api
from polyrides import db
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


def main():
    """Set up and run the Flask app."""
    args = _parse_args()

    api.add_resource(users.Users, '/users')
    api.add_resource(users.UserById, '/users/<int:user_id>')

    app.debug = args.debug
    app.run(port=args.port)


if __name__ == '__main__':
    main()
