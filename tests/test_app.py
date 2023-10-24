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
