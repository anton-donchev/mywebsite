from nose.tools import assert_in
from flask import url_for

from tests import app, client

class TestForms:
    def test_registration_form(self):
        data = {"username":  "boss", # NOTE: username already in db.
                "password":  "4321",
                "password2": "4321",
                "email":     "boss@vip.com"}
        url = url_for("main.register")
        response = client.post(url, follow_redirects=True, data=data)
        # If 'password2' field, user is still on registration page.
        assert_in(b"password2", response.data)
        # Username not in db, however email is (should be rejected).
        data["username"] = "main_boss"
        data["email"] = "bs@bs.com"
        response = client.post(url, follow_redirects=True, data=data)
        assert_in(b"password2", response.data)
