from lib.models import *
from hashlib import sha256


def seed_database():
    # drop tables first
    Booking.drop_table()
    Listing.drop_table()
    User.drop_table()

    # create tables
    create_db_tables()

    # create test users
    User.create(email='jdoe@gmail.com', password=sha256('jdoepassword'.encode()).hexdigest())
    User.create(email='kmoor@outlook.com', password=sha256('kmoorpassword'.encode()).hexdigest())

    # create test listings
    Listing.create(title='My House', description='A nice house', price=100, start_date='2023-11-24', end_date='2023-12-01', owner=1)
    Listing.create(title='My Flat', description='Small but cosy', price=50, start_date='2023-11-14', end_date='2023-11-21', owner=2)

    # create test booking
    Booking.create(start_date='2023-11-24', end_date='2023-11-25', listing=1, user=2, approved=False)
    Booking.create(start_date='2023-11-17', end_date='2023-11-18', listing=2, user=1, approved=False)
    Booking.create(start_date='2023-11-17', end_date='2023-11-18', listing=2, user=1, approved=False)