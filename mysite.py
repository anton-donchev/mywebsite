#!/usr/bin/env python
# coding=utf-8

from mywebsite import app, db
from mywebsite.models import Admin


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Admin": Admin}
