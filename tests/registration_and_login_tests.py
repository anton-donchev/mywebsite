import os

from nose.tools import assert_equal, assert_in, assert_not_in
from flask import url_for

from tests import app, client


class TestLoginAndRegister:
    def test_1_register(self):
        data = {"username":  "smaug",
                "password":  "sM@Wg1",
                "password2": "sM@Wg11", # NOTE: Repeated password mismatch.
                "email":     "smaug@theterrible.com"}
        url = url_for("main.register")
        response = client.post(url, follow_redirects=True, data=data)
        assert_equal(response.status_code, 200)
        # If 'password2' field, user is still on registration page.
        assert_in(b"password2", response.data)

        data["password2"] = "sM@Wg1" # Repeated password match.
        response = client.post(url, follow_redirects=True, data=data)
        assert_equal(response.status_code, 200)
        # No "password2" field, meaning pass accepted and redirect triggered.
        assert_not_in(b"password2", response.data)

    def test_2_login(self):
        # Check arbitrary credentials login (should be denied).
        data = {"user_or_mail": "hfshfvnbryr",
                "password": "645jtgrnj"}
        url = url_for("main.login")
        response = client.post(url, follow_redirects=True, data=data)
        assert_equal(response.status_code, 200)
        # If "password" field, user still on login page - login denied.
        assert_in(b"password", response.data)
        # Check login for user with a "pending" status (should be denied).
        data = {"user_or_mail": "smaug", "password": "sM@Wg1"}
        response = client.post(url, follow_redirects=True, data=data)
        assert_equal(response.status_code, 200)
        assert_in(b"password", response.data)
        # Check login for an active admin (should be accepted).
        data = {"user_or_mail": "boss", "password": "1234"}
        response = client.post(url, follow_redirects=True, data=data)
        assert_equal(response.status_code, 200)
        # No "password" field, meaning credentials accepted and user redirected.
        assert_not_in(b"password", response.data)
        # Check whether admin is acknowledged on the redirected page.
        username_bytes = "boss".encode(encoding="UTF-8", errors="strict")
        assert_in(username_bytes, response.data)
        # Check if logged in user is redirected from login and registration.
        response = client.get(url)
        assert_equal(response.status_code, 302)
        response = client.get(url_for("main.register"))
        assert_equal(response.status_code, 302)

    def test_3_logout(self):
        response = client.get("/logout", follow_redirects=True)
        assert_equal(response.status_code, 200)
        username_bytes = "boss".encode(encoding="UTF-8", errors="strict")
        assert_not_in(username_bytes, response.data)
