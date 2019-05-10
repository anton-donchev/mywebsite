#!/usr/bin/env python
# coding=utf-8

import os


rootdir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "8~F07bo?0.');(P\w3kUk6N\hV?)C"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
        "sqlite:///" + os.path.join(rootdir, 'mywebsite_data_dev.sqlite')


class TestsConfig(Config):
    TESTING = True
    SERVER_NAME = "127.0.0.1:5000"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite://"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(rootdir, 'mywebsite_data.sqlite')


config = {
    'development': DevelopmentConfig,
    'tests':       TestsConfig,
    'production':  ProductionConfig,

    'default':     DevelopmentConfig
}
