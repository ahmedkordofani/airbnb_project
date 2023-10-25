from lib.validator import Validator
from datetime import datetime

def test_valid_password():
    vd = Validator()

    # test with valid data for empty list of errors
    assert vd.validate_signup('jdoe@gmail.com', '1@Password', '1@Password') == []

def test_invalid_passwords():
    vd = Validator()

    # test with empty password
    assert len(vd.validate_signup('jdoe@gmail.com', '', '')) == 4

    # test when passwords don't match
    assert vd.validate_signup('jdoe@gmail.com', '1@Password', '1@Password1') == ['Passwords must match']

def test_valid_emails():
    vd = Validator()

    assert vd.validate_signup('jdoe@outlook.io', '1@Password', '1@Password') == []

def test_invalid_emails():
    vd = Validator()

    # test empty email
    assert vd.validate_signup('', '1@Password', '1@Password') == ['Email cannot be blank']

    # test no @ symbol
    assert vd.validate_signup('jdoegmail.com', '1@Password', '1@Password') == ['Email must be valid']

    # test no .com
    assert vd.validate_signup('jdoe@outlook', '1@Password', '1@Password') == ['Email must be valid']

    # test no domain
    assert vd.validate_signup('jdoe@.com', '1@Password', '1@Password') == ['Email must be valid']

def test_validate_listing():
    vd = Validator()

    # test empty title
    assert vd.validate_listing('', 'description', 1, '24/11/2023', '27/11/2023') == ['Title cannot be blank']

    # test empty description
    assert vd.validate_listing('title', '', 1, '24/11/2023', '27/11/2023') == ['Description cannot be blank']

    # test negative price
    assert vd.validate_listing('title', 'description', -1, '24/11/2023', '27/11/2023') == ['Price cannot be negative']

    # test empty start date
    assert vd.validate_listing('title', 'description', 1, '', '27/11/2023') == ['Start date must be valid']

    # test empty end date
    assert vd.validate_listing('title', 'description', 1, '24/11/2023', '') == ['End date must be valid']

    # test end date before start date
    assert vd.validate_listing('title', 'description', 1, '27/11/2023', '24/11/2023') == ['End date must be after start date']

    # test start date in the past
    assert vd.validate_listing('title', 'description', 1, '24/03/2023', '27/11/2023') == ['Start date cannot be in the past']

    # test valid listing
    assert vd.validate_listing('title', 'description', 1, '24/11/2023', '27/11/2023') == []
