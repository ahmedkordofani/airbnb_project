from playwright.sync_api import Page, expect
from seeds.seed_db import *

# Tests for your routes go here

"""
We can render the index page
"""


def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/")

    # We look at the <p> tag
    strong_tag = page.locator("p")

    # We assert that it has the text "This is the homepage."
    expect(strong_tag).to_have_text("This is the homepage.")


def test_get_signup_form(page, test_web_address):
    page.goto(f"http://{test_web_address}/signup")
    form = page.locator(".sign-up-form")
    expect(form).to_have_count(1)


def test_signup_success(page, test_web_address):
    seed_database()

    page.goto(f"http://{test_web_address}/signup")

    email_box = page.locator("#email")
    email_box.fill("benchmark@gmail.com")

    password_box = page.locator("#password")
    password_box.fill("1@Password")

    password_repeat_box = page.locator("#password-repeat")
    password_repeat_box.fill("1@Password")

    submit_button = page.locator("#submit")
    submit_button.click()

    assert page.url == f"http://{test_web_address}/"
    
    user = User.select().where(User.email == "benchmark@gmail.com").get()
    assert user.email == "benchmark@gmail.com"

def test_signup_fail(page, test_web_address):
    seed_database()

    page.goto(f"http://{test_web_address}/signup")

    email_box = page.locator("#email")
    email_box.fill("benchmark@gmail.com")

    password_box = page.locator("#password")
    password_box.fill("1Password")

    password_repeat_box = page.locator("#password-repeat")
    password_repeat_box.fill("1Password")

    submit_button = page.locator("#submit")
    submit_button.click()

    assert page.url == f"http://{test_web_address}/signup"

    page.screenshot(path="screenshot.png")

    error = page.locator(".error")
    expect(error).to_have_count(1)

def test_get_login_form(page, test_web_address):
    page.goto(f"http://{test_web_address}/login")
    form = page.locator(".log-in-form")
    expect(form).to_have_count(1)

def test_login_success(page, test_web_address):
    seed_database()

    page.goto(f"http://{test_web_address}/login")

    email_box = page.locator("#email")
    email_box.fill("jdoe@gmail.com")

    password_box = page.locator("#password")
    password_box.fill("jdoepassword")

    submit_button = page.locator("#submit-login")
    submit_button.click()

    assert page.url == f"http://{test_web_address}/"

def test_login_fail(page, test_web_address):
    seed_database()

    page.goto(f"http://{test_web_address}/login")

    email_box = page.locator("#email")
    email_box.fill("jdoe@gmail.com")

    password_box = page.locator("#password")
    password_box.fill("jdoepassword123")

    submit_button = page.locator("#submit-login")
    submit_button.click()

    assert page.url == f"http://{test_web_address}/login"

def test_create_listing(page, test_web_address):
    seed_database()

    page.goto(f"http://{test_web_address}/login")

    email_box = page.locator("#email")
    email_box.fill("jdoe@gmail.com")

    password_box = page.locator("#password")
    password_box.fill("jdoepassword")

    submit_button = page.locator("#submit-login")
    submit_button.click()

    page.goto(f"http://{test_web_address}/spaces/new")

    name_box = page.locator("#name")
    name_box.fill("Test Listing")

    description_box = page.locator("#description")
    description_box.fill("Test Description")

    price_box = page.locator("#price")
    price_box.fill("100")

    start_date_box = page.locator("available-from")
    start_date_box.fill("24/11/2024")

    end_date_box = page.locator("#available-to")
    end_date_box.fill("27/11/2024")

    submit_button = page.locator("#submit-listing")
    submit_button.click()

    assert page.url == f'http://{test_web_address}/'