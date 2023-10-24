from seeds.seed_db import *

def test_email_exists():
    seed_database()

    assert User.check_email_exists('jdoe@gmail.com')
    assert not User.check_email_exists('example@outlook.com')

def test_login_checks():
    seed_database()

    assert User.check_login_success('jdoe@gmail.com', 'jdoepassword')
    assert not User.check_login_success('jdoe@gmail.com', 'wrongpassword')