#!/usr/bin/env python

#chmod +x ride_model_test.py

from polyrides.models.location import Location
from polyrides.models.ride import Ride
from polyrides.models.time_range import TimeRange
from polyrides.models.user import User
from datetime import datetime



slo = Location(
    name='San Luis Obispo'
)
slo.create()
sf = Location(
    name='San Francisco'
)
sf.create()
r = Ride( 
    start_location_id=1,
    destination_id=2,
    departure_date = datetime(2015, 6, 5),
    capacity = 4,
    driver_id = 1,
    time_range_id = 1
)
r.create()
tr = TimeRange(
    description = 'Early Morning',
    start_time = '5',
    end_time='9'
)
tr.create()
u = User(
    first_name = 'ollie',
    last_name = 'wang',
    email = 'owang@calpoly.edu',
    password = 'password'
)
u.create()
u2 = User(
    first_name = 'quan',
    last_name = 'tran',
    email = 'qtran@calpoly.edu',
    password = 'password123'
)
u2.create()
u3 = User(
    first_name = 'phil',
    last_name = 'daniel',
    email = 'pdaniel@calpoly.edu',
    password = 'password321'
)
u3.create()

print(User.query.all())
print(TimeRange.query.all())
print(Ride.query.all())

print("Append quan and phil to ride 1 ")

r.passengers.append(User.query.filter(User.id == u2.id).first())
r.passengers.append(User.query.filter(User.id == u3.id).first())


print(r.time_range.description)
print("  Start  " +str(r.time_range.start_time))
print("  {}".format(slo.name))
print("  End  " + str(r.time_range.end_time))
print("  {}".format(sf.name))
print()
print("PASSENGERS")
for passenger in r.passengers:
    print("first name: " + passenger.first_name)
    print("last name: " + passenger.last_name)
