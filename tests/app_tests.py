import os

from nose.tools import assert_true

from tests import app, client


class TestApp:
    def test_app_existence(self):
        assert_true(app is not None)

    def test_app_testing_mode(self):
        assert_true(app.config['TESTING'])
