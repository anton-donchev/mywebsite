import os

from mywebsite import create_app, db
from mywebsite.models import Admin


app = create_app("tests")
client = app.test_client()


def setup():
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    admin = Admin(username="boss", email="bs@bs.com", password="1234", status="active")
    db.session.add(admin)
    db.session.commit()


def teardown():
    db.session.remove()
    db.drop_all()
