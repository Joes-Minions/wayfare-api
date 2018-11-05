#!/usr/bin/env python

#chmod +x ride_model_test.py

from polyrides.models.ride import Ride
from polyrides.models.user import User
from polyrides.models.time_range import TimeRange
from datetime import datetime


r = Ride( 
    # start_location='fremont',
    # end_location='sanluis', 
    departure_date = datetime(2015, 6, 5),
    ride_capacity = 4,
    driver_id = 1,
    time_range_id = 1
)

tr = TimeRange(
    description = 'Early Morning',
    start_time = '5',
    end_time='9'
)
u = User(
    first_name = 'ollie',
    last_name = 'wang',
    email = 'owang@calpoly.edu',
    password = 'password'
)

u2 = User(
    first_name = 'quan',
    last_name = 'tran',
    email = 'qtran@calpoly.edu',
    password = 'password123'
)
u3 = User(
    first_name = 'phil',
    last_name = 'daniel',
    email = 'pdaniel@calpoly.edu',
    password = 'password321'
)
tr.create()
r.create()
u.create()
u2.create()
u3.create()

print(User.query.all())
print(TimeRange.query.all())
print(Ride.query.all())

print("Append quan and phil to ride 1 ")

r.passengers.append(User.query.filter(User.id == u2.id).first())
r.passengers.append(User.query.filter(User.id == u3.id).first())

print(r.time_range.description)
print("  Start  " +str(r.time_range.start_time))
print("  End  " + str(r.time_range.end_time))
print("PASSENGERS")
for passenger in r.passengers:
    print("first name: " + passenger.first_name)
    print("last name: " + passenger.last_name)
