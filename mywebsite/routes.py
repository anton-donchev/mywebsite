from flask import render_template, flash, redirect, url_for
from mywebsite import app
from mywebsite.forms import LoginForm


@app.route("/")
@app.route("/index")
@app.route("/home")
def home():
    return "This works."


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash(f"Log in requested from user {login_form.username.data},\
              remember_me={login_form.remember_me.data}.")
        return redirect(url_for("login"))
    return render_template("login.html", title="Sign In", login_form=login_form)
