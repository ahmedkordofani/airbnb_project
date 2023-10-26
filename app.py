import os
from flask import Flask, request, render_template, redirect, session
from lib.models import *
from lib.validator import Validator
from hashlib import sha256


# Create a new Flask app
app = Flask(__name__)
create_db_tables()

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5000/index


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')


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
        return redirect("/")
    else:
        return render_template('login.html', success=success, logged_in=True if 'user_id' in session else False)
    
@app.route('/logout', methods=['GET'])
def logout():
    try:
        session.pop("user_id")
    except:
        pass
    return redirect("/")

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
                start_date=datetime.strptime(start_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
                end_date=datetime.strptime(end_date, "%d/%m/%Y").strftime("%Y-%m-%d"),
                owner=session['user_id']
                )
            return redirect("/spaces")
        else:
            return render_template('listaspace.html', errors=errors, logged_in=True if 'user_id' in session else False)

@app.route('/spaces', methods=['GET'])
def list_spaces():

    if 'user_id' not in session:
        return redirect("/login")

    spaces = Listing.get_all()

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
        spaces = Listing.get_by_date(datetime.strptime(start_date, '%d/%m/%Y'), datetime.strptime(end_date, '%d/%m/%Y'))
        return render_template('bookaspace.html', spaces=spaces, logged_in=True if 'user_id' in session else False)
    else:
        spaces = Listing.get_all()
        return render_template('bookaspace.html', errors=errors, spaces=spaces, logged_in=True if 'user_id' in session else False)

@app.route('/spaces/<int:listing_id>', methods=['GET'])
def list_date_selection(listing_id):

    if 'user_id' not in session:
        return redirect("/login")

    listing = Listing.get_by_id(listing_id)

    return render_template('spaces.html', listing=listing, logged_in=True if 'user_id' in session else False)

@app.route('/spaces/<int:listing_id>', methods=['POST'])
def create_booking(listing_id):

    if 'user_id' not in session:
        return redirect("/login")
    
    else:
        Booking.create(
            start_date=datetime.strptime(request.form["available-from"], "%d/%m/%Y").strftime("%Y-%m-%d"),
            end_date=datetime.strptime(request.form["available-to"], "%d/%m/%Y").strftime("%Y-%m-%d"),
            listing=listing_id,
            user=session['user_id']
        )
        return redirect("/spaces")

@app.route('/requests', methods=['GET'])
def list_requests():

    if 'user_id' not in session:
        return redirect("/login")
    else:
        requests = Booking.select().join(Listing).where(Booking.listing.owner == session['user_id'])
        booked_spaces = Booking.select().where(Booking.user == session['user_id'])


        #return render_template('requests.html', booked_spaces=booked_spaces, requests=requests, logged_in=True if 'user_id' in session else False)

@app.route('/requests/<int:booking_id>', methods=['GET'])
def get_request_details(booking_id):

    if 'user_id' not in session:
        return redirect("/login")
    
    try:
        booking = Booking.select().join(Listing).where(Booking.id == booking_id).get()
    except:
        return redirect("/requests")
    
    if session['user_id'] != booking.listing.owner:
        return redirect("/requests")

    other_bookings = Booking.select().where(Booking.start_date == booking.start_date, Booking.id != booking.id)
    
    # return render template for request details

@app.route('/requests/<int:booking_id>/confirm', methods=['POST'])
def confirm_booking_request(booking_id):

    if 'user_id' not in session:
        return redirect("/login")
    
    try:
        booking = Booking.select().join(Listing).where(Booking.id == booking_id).get()
    except:
        return redirect("/requests")
    
    if session['user_id'] != booking.listing.owner:
        return redirect("/requests")
    else:
        booking.approved = True
        booking.save()

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
    
    if session['user_id'] != booking.listing.owner:
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
