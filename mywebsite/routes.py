#!/usr/bin/env python
# coding=utf-8

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_
from werkzeug.urls import url_parse

from mysite import app
from mywebsite.forms import LoginForm, RegistrationForm
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
        admin = Admin.query.filter_by(status="active").\
            filter(
                or_(Admin.username==login_form.user_or_mail.data,
                    Admin.email==(login_form.user_or_mail.data).lower())
                    ).first()
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


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for("home"))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        admin = Admin(username=registration_form.username.data,
                      email=registration_form.email.data,
                      status="pending")
        admin.set_password(registration_form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash("Request for admin rights sent."
              "\nYou will be notified if your request is granted.")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register",
                           registration_form=registration_form)
