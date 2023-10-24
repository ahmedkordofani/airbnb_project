import os
from flask import Flask, request, render_template, redirect
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
    return render_template('signup.html')

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
        return redirect("/")


    


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
