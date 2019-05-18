#!/usr/bin/env python
# coding=utf-8

from flask import render_template, flash, redirect, url_for, request
from flask import current_app
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_
from werkzeug.urls import url_parse
from datetime import datetime

from mywebsite import db
from mywebsite import main_blueprint as main
from mywebsite.forms import LoginForm, RegistrationForm, ChangePasswordForm
from mywebsite.models import Admin


@main.before_request
def update_timestamp():
    if current_user.is_authenticated:
        current_user.timestamp = datetime.utcnow()
        db.session.commit()


@main.route("/")
@main.route("/index")
@main.route("/home")
def home():
    current_app.logger.info("Get request to home page.")
    return render_template("home.html", title="Home")


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for(".home"))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        admin = Admin.query.filter_by(status="active").\
            filter(
                or_(Admin.username==login_form.user_or_mail.data,
                    Admin.email==(login_form.user_or_mail.data).lower())
                    ).first()
        if admin is None or not admin.check_password(login_form.password.data):
            current_app.logger.info(
                f"Failed login attempt for: '{login_form.user_or_mail.data}'"
                )
            flash("Invalid username or password.")
            return redirect(url_for(".login"))
        login_user(admin, remember=login_form.remember_me.data)
        current_app.logger.info(
            f"Admin '{current_user.username}' logged in."
            )
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for(".home")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", login_form=login_form)


@main.route("/logout")
def logout():
    if not current_app.config["TESTING"]:
        current_app.logger.info(f"Admin '{current_user.username}' logging out.")
    logout_user()
    return redirect(url_for(".home"))


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        current_app.logger.info(
            f"Admin '{current_user.username}' is already logged in."
            )
        flash("You are already logged in.")
        return redirect(url_for(".home"))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        admin = Admin(username=registration_form.username.data,
                      email=registration_form.email.data,
                      password=registration_form.password.data,
                      status="pending")
        db.session.add(admin)
        db.session.commit()
        current_app.logger.info(
            f"User '{registration_form.username.data}' requested admin rights."
            )
        flash("Request for admin rights sent."
              "\nYou will be notified if your request is granted.")
        return redirect(url_for(".login"))
    return render_template("register.html", title="Register",
                           registration_form=registration_form)


@main.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    current_app.logger.info(
        f"Admin '{current_user.username}' accessed the admin panel."
        )
    admins = Admin.query.all()
    get_admin = lambda admin_id: Admin.query.filter_by(id=admin_id).first()
    change_password_form = ChangePasswordForm()

    if request.method == "POST":

        if change_password_form.validate_on_submit():
            print(">>>> routes.py, admin(), change_password_form validated.")

        if request.form.get("show_password_form"):
            flash(f"Admin '{current_user.username}' requested password change.")
        elif request.form.get("deactivate_admin"):
            admin_id = request.form.get("deactivate_admin")
            admin = get_admin(admin_id)
            admin.status = "inactive"
            flash(f"Admin rights removed for user '{admin.username}'.")
        elif request.form.get("reject_user"):
            admin_id = request.form.get("reject_user")
            admin = get_admin(admin_id)
            admin.status = "inactive"
            flash(f"Request for admin rights rejected for: '{admin.username}'.")
        elif request.form.get("accept_user"):
            admin_id = request.form.get("accept_user")
            admin = get_admin(admin_id)
            admin.status = "active"
            flash(f"Admin rights granted to user: '{admin.username}'.")
        elif request.form.get("activate_admin"):
            admin_id = request.form.get("activate_admin")
            admin = get_admin(admin_id)
            admin.status = "active"
            flash(f"Admin rights granted to user: '{admin.username}'.")
        else:
            current_app.logger.error(
                f"Unexpected POST request to '/admin': {request.form}"
                )

        db.session.commit()
        return redirect(url_for(".admin"))

    return render_template("admin.html", title="Admin", admins=admins,
                           change_password_form=change_password_form)
