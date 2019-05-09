#!/usr/bin/env python
# coding=utf-8

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from mywebsite import create_app, db
from mywebsite.models import Admin
from flask_migrate import Migrate, upgrade

app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)

from mywebsite import routes, models


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Admin": Admin}
