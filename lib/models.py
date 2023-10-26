import peewee
import os
from datetime import datetime
from hashlib import sha256

# Connect to relevant database
if os.environ.get('APP_ENV') == 'test':
    db = peewee.PostgresqlDatabase(
        'airbnb-test', host='localhost', port=5432, user='postgres', password='postgres')
elif os.environ.get('APP_ENV') == 'prod':
    db = peewee.PostgresqlDatabase(
        't3_airbnb_database', 
        host=os.environ.get('POSTGRES_HOSTNAME'), 
        port=5432, 
        user='t3', 
        password=os.environ.get('POSTGRES_PASSWORD'))
else:
    db = peewee.PostgresqlDatabase('airbnb-dev')

# define our models

# User model
class User(peewee.Model):

    # fields
    email = peewee.CharField()
    password = peewee.CharField()

    # meta class
    class Meta:
        database = db
        table_name = 'users'

    def check_email_exists(email):
        try:
            User.select(User.email).where(User.email == email).get()
            return True
        except:
            return False

    def check_login_success(email, password):

        # hash password
        enc_pw = sha256(password.encode()).hexdigest()

        try:
            User.select().where(User.email == email and User.password == enc_pw).get()
            return True
        except:
            return False


# Listing model
class Listing(peewee.Model):

    # fields
    title = peewee.CharField()
    description = peewee.TextField()
    price = peewee.DecimalField()
    start_date = peewee.DateField(default=datetime.now)
    end_date = peewee.DateField()
    owner = peewee.ForeignKeyField(User, backref='listings')

    # meta class
    class Meta:
        database = db
        table_name = 'listings'

    def get_by_date(target_start_date, target_end_date):
        listings = Listing.select().where(
            Listing.start_date <= target_start_date, target_end_date <= Listing.end_date
            )
        return [listing for listing in listings]

    def get_all():
        listings = Listing.select().where(Listing.end_date > datetime.today())
        return [listing for listing in listings]


# Booking model
class Booking(peewee.Model):

    # fields
    start_date = peewee.DateField()
    end_date = peewee.DateField()
    listing = peewee.ForeignKeyField(Listing, backref='bookings')
    user = peewee.ForeignKeyField(User, backref='bookings')
    approved = peewee.BooleanField(default=False)

    # meta class
    class Meta:
        database = db
        table_name = 'bookings'
    
    def cancel_other_bookings(conf_booking):
        bookings = Booking.select().where(Booking.start_date == conf_booking.start_date)
        try:
            for booking in bookings:
                Booking.delete_by_id(booking.id)
        except:
            pass


# create tables
def create_db_tables():
    with db:
        db.create_tables([User, Listing, Booking])
