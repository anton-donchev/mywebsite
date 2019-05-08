#!/usr/bin/env python
# coding=utf-8

import os


rootdir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY") or "8~F07bo?0.');(P\w3kUk6N\hV?)C"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
        "sqlite:///" + os.path.join(rootdir, 'mywebsite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
