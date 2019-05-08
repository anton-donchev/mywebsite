#!/usr/bin/env python
# coding=utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "name":             "MyWebsite",
    "description":      "A flexible framework for creating simple personal websites.",
    "author":           "Anton Donchev",
    "url":              "",
    "author_email":     "donchev.anton@gmail.com",
    "version":          "0.0.1",
    "install_requires": ["nose", "python-dotenv", "flask", "flask-wtf",
                         "flask-sqlalchemy", "flask-migrate", "flask-login"],
    "packages":         ["website", "tests", "bin"],
    "scripts":          [],
}

setup(**config)
