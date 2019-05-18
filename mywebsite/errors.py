from flask import render_template, request, current_app

from mywebsite import db
from mywebsite import main_blueprint as main


@main.errorhandler(404)
def not_found_error(error):
    current_app.logger.warning(f"404 error for request: f{request.path}")
    return render_template("404.html"), 404


@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500
