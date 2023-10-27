import os, smtplib, ssl
from flask import Flask, request, render_template, redirect, session
from lib.models import *
from lib.validator import Validator
from hashlib import sha256
from email.message import EmailMessage
from threading import Thread
from json import dumps
from datetime import timedelta

# email info globals
EMAIL_ADDR = os.environ.get('EMAIL_ADDR')
GMAIL_APP_PW = os.environ.get('GMAIL_APP_PW')

# function for emailing
def send_email(receiver, subject, content):
    # stop function if no email or password found
    if EMAIL_ADDR is None or GMAIL_APP_PW is None:
        return None
    
    em = EmailMessage()
    em.set_content(content)
    em['Subject'] = subject
    em['From'] = EMAIL_ADDR
    em['To'] = receiver
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as s:
        s.login(EMAIL_ADDR, GMAIL_APP_PW)
        s.sendmail(EMAIL_ADDR, [receiver], em.as_string())

# Create a new Flask app
app = Flask(__name__)
create_db_tables()

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index


@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')

@app.route('/', methods=['GET'])
def get_index_redirect():
    return redirect("/login")

@app.route('/signup', methods=['GET'])
def get_signup_form():
    return render_template('signup.html', logged_in = True if 'user_id' in session else False)

@app.route('/signup', methods=['POST'])
def post_signup_form():
    vd = Validator()
    email = request.form["email"]
    password = request.form["password"]
    password_repeat = request.form["password-repeat"]

    errors = vd.validate_signup(email, password, password_repeat)
    existing_user = User.check_email_exists(email)

    if not existing_user and not errors:
        User.create(email=email, password=sha256(password.encode()).hexdigest())

        # send email
        Thread(target=send_email, args=(email, "Welcome to AirBnB", "Welcome to AirBnB!")).start()

        return redirect("/login")
    else:
        return render_template('signup.html', errors=errors, logged_in=True if 'user_id' in session else False)

@app.route('/login', methods=['GET'])
def get_login_form():
    return render_template('login.html', success=True, logged_in = True if 'user_id' in session else False)

@app.route('/login', methods=['POST'])
def post_login_form():
    email = request.form["email"]
    password = request.form["password"]

    success = User.check_login_success(email, password)

    if success:
        session["user_id"] = User.select(User.id).where(User.email == email).get().id
        return redirect("/spaces")
    else:
        return render_template('login.html', success=success, logged_in=True if 'user_id' in session else False)
    
@app.route('/logout', methods=['GET'])
def logout():
    try:
        session.pop("user_id")
    except:
        pass
    return redirect("/login")

@app.route('/spaces/new', methods=['GET'])
def get_listaspace():

    if 'user_id' in session:
        return render_template('listaspace.html', logged_in=True if 'user_id' in session else False)
    else:
        return redirect("/login")

@app.route('/spaces/new', methods=['POST'])
def create_listing():

    if 'user_id' not in session:
        return redirect("/login")
    else:

        vd = Validator()

        title = request.form["name"]
        description = request.form["description"]
        price = float(request.form["price"])
        start_date = request.form["available-from"]
        end_date = request.form["available-to"]

        errors = vd.validate_listing(title, description, price, start_date, end_date)

        if not errors:
            Listing.create(
                title=title, 
                description=description, 
                price=price, 
                start_date=start_date,
                end_date=end_date,
                owner=session['user_id']
                )
            new_id = Listing.select().order_by(Listing.id.desc()).get().id
            return redirect(f"/spaces/{new_id}")
        else:
            return render_template('listaspace.html', errors=errors, logged_in=True if 'user_id' in session else False)

@app.route('/spaces', methods=['GET'])
def list_spaces():

    if 'user_id' not in session:
        return redirect("/login")

    spaces = sorted(Listing.get_all(), key=lambda x: x.start_date)

    return render_template('bookaspace.html', spaces=spaces, logged_in=True if 'user_id' in session else False)

@app.route('/spaces/search', methods=['POST'])
def list_search_spaces():

    if 'user_id' not in session:
        return redirect("/login")
    
    vd = Validator()

    start_date = request.form["available-from"]
    end_date = request.form["available-to"]

    errors = vd.validate_listing_search(start_date, end_date)

    if not errors:
        spaces = sorted(Listing.get_by_date(start_date, end_date), key=lambda x: x.start_date)
        return render_template('bookaspace.html', spaces=spaces, logged_in=True if 'user_id' in session else False)
    else:
        spaces = sorted(Listing.get_all(), key=lambda x: x.start_date)
        return render_template('bookaspace.html', errors=errors, spaces=spaces, logged_in=True if 'user_id' in session else False)

@app.route('/spaces/<int:listing_id>', methods=['GET'])
def list_date_selection(listing_id):

    if 'user_id' not in session:
        return redirect("/login")

    listing = Listing.get_by_id(listing_id)

    return render_template('spaces.html', listing_id=dumps(listing_id), listing=listing, logged_in=True if 'user_id' in session else False)

@app.route('/spaces/<int:listing_id>', methods=['POST'])
def create_booking(listing_id):

    if 'user_id' not in session:
        return redirect("/login")
    
    else:
        date = datetime.strptime(request.form['selectedDate'], '%Y-%m-%d')

        Booking.create(
            start_date=date,
            end_date= date + timedelta(days=1),
            listing=listing_id,
            user=session['user_id']
        )
        listing = Listing.select().where(Listing.id == listing_id).get()
        email = User.select().where(User.id == listing.owner).get().email

        # send email
        Thread(target=send_email, args=(email, "You have received a booking request!", 
                                        f"You have received a booking request:\n\nSpace: {listing.title}\n\nDate: {date.strftime('%Y-%m-%d')}\n\nPlease login to your account to approve or decline the request.")
                                        ).start()

        return redirect("/spaces")

@app.route('/requests', methods=['GET'])
def list_requests():

    if 'user_id' not in session:
        return redirect("/login")
    else:
        requests = Booking.select().join(Listing).where(Booking.listing.owner == session['user_id'], Booking.approved == False)
        booked_spaces = Booking.select().where(Booking.user == session['user_id'])


        return render_template('requests.html', booked_spaces=booked_spaces, requests=requests, logged_in=True if 'user_id' in session else False)

@app.route('/requests/<int:booking_id>', methods=['GET'])
def get_request_details(booking_id):

    if 'user_id' not in session:
        return redirect("/login")
    
    try:
        booking = Booking.select().join(Listing).where(Booking.id == booking_id).get()
    except:
        return redirect("/requests")
    
    if session['user_id'] != booking.listing.owner.id:
        return redirect("/requests")

    other_bookings = Booking.select().where(Booking.start_date == booking.start_date, Booking.id != booking.id)
    
    return render_template('request_for.html', booking=booking, other_bookings=other_bookings, logged_in=True if 'user_id' in session else False)

@app.route('/requests/<int:booking_id>/confirm', methods=['POST'])
def confirm_booking_request(booking_id):

    if 'user_id' not in session:
        return redirect("/login")
    
    try:
        booking = Booking.select().join(Listing).where(Booking.id == booking_id).get()
    except:
        return redirect("/requests")
    
    if session['user_id'] != booking.listing.owner.id:
        return redirect("/requests")
    else:
        Booking.update(approved=True).where(Booking.id == booking_id).execute()

        # send confirmation email
        email = User.select().where(User.id == booking.user).get().email
        Thread(target=send_email, args=(email, "Booking Confirmation", "Your booking has been confirmed!")).start()

        # cancel other bookings
        Booking.cancel_other_bookings(booking)

    return redirect("/requests")

@app.route('/requests/<int:booking_id>/decline', methods=['POST'])
def decline_booking_request(booking_id):

    if 'user_id' not in session:
        return redirect("/login")
    
    try:
        booking = Booking.select().join(Listing).where(Booking.id == booking_id).get()
    except:
        return redirect("/requests")
    
    if session['user_id'] != booking.listing.owner.id:
        return redirect("/requests")
    else:
        Booking.delete_by_id(booking_id)

    return redirect("/requests")



# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    if os.environ.get('APP_ENV') not in ['prod', 'test']:
        app.secret_key = os.urandom(24)
        app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
    else:
        app.secret_key = os.urandom(24)
        app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
