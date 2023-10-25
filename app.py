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
            return redirect("/")
        else:
            return render_template('listaspace.html', errors=errors, logged_in=True if 'user_id' in session else False)


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
