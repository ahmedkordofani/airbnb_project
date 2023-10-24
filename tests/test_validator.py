from lib.validator import Validator

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
