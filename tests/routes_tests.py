import os

from nose.tools import assert_equal
from mywebsite import db


class TestRoutes:
    def setup(self):
        os.environ["FLASK_CONFIG"] = "tests"
        from mysite import app
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        # db.create_all()
        self.rules = [str(r) for r in self.app.url_map.iter_rules()]

    def teardown(self):
        # db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def test_every_route(self):
        for rule in self.rules:
            response = self.client.get(rule)
            print(f">>>> Testing routes: rule = {rule}, response = {response}.")
            if rule == "/static/<path:filename>":
                assert_equal(response.status_code, 404)
            elif rule == "/logout":
                assert_equal(response.status_code, 302)
            else:
                assert_equal(response.status_code, 200)
