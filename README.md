# MakersBnB Python Project Seed

This repo contains the seed codebase for the MakersBnB project in Python (using 
Flask and Pytest).

Someone in your team should fork this seed repo to their Github account. 
Everyone in the team should then clone this fork to their local machine to work on it.

## Setup

```shell
# Install dependencies and set up the virtual environment
; pipenv install

# Activate the virtual environment
; pipenv shell

# Install the virtual browser we will use for testing
; playwright install
# If you have problems with the above, contact your coach

# Create a test and development database
; createdb airbnb-dev

# create .env file
; echo "export APP_ENV='dev'" > .env

# Run the tests (with extra logging)
; pipenv run pytest -x

# Run the app
; pipenv run python3 app.py

# Now visit http://localhost:5000/index in your browser
```