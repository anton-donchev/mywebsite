import os

from flask import url_for
from nose.tools import assert_equal

from tests import app, client


class TestRoutes:
    def test_every_route(self):
        client.get(url_for("main.logout"))
        rules = [str(r) for r in app.url_map.iter_rules()]
        for rule in rules:
            response = client.get(rule)
            print(f">>>> Testing routes: rule = {rule}, response = {response}.")
            if rule == "/static/<path:filename>":
                assert_equal(response.status_code, 404)
            elif rule == "/logout" or rule == "/admin":
                assert_equal(response.status_code, 302)
            else:
                assert_equal(response.status_code, 200)
