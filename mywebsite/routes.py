#!/usr/bin/env python
# coding=utf-8

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from mywebsite import app
from mywebsite.forms import LoginForm
from mywebsite.models import Admin


@app.route("/")
@app.route("/index")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for("home"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        admin = Admin.query.filter_by(username=login_form.username.data).first()
        if admin is None or not admin.check_password(login_form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for("login"))
        login_user(admin, remember=login_form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("home")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", login_form=login_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
