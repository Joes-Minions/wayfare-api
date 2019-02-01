"""The main driver and entrypoint for the Wayfare API."""
import argparse

from wayfare import app
from wayfare import api
from wayfare.routes import users
from wayfare.routes import rides
from wayfare.routes import passengers


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
    args = parser.parse_args()
    return args


def main():
    """Set up and run the Flask app."""
    args = _parse_args()

    api.add_resource(users.Users, users.BASE_URL)
    api.add_resource(users.UserById, f'{users.BASE_URL}/<int:user_id>')
    api.add_resource(rides.Rides, rides.BASE_URL)
    api.add_resource(rides.RidesById, f'{rides.BASE_URL}/<int:ride_id>')
    api.add_resource(passengers.Passengers,
        f'{passengers.BASE_URL}/<int:ride_id>/users')
    api.add_resource(passengers.PassengersById,
        f'{passengers.BASE_URL}/<int:ride_id>/users/<int:user_id>')

    app.debug = args.debug
    app.run(port=args.port)
    

if __name__ == '__main__':
    main()
