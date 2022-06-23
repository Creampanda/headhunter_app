#!/usr/bin/env python3

import os
from flask import (
    Flask,
    request,
    abort,
    g,
    jsonify,
    render_template
)
import psycopg2
from werkzeug.urls import url_encode

import sys

sys.path.insert(1, "..")

import logging
import jinja2


DATETIME_FMT = "%Y-%m-%dT%H-%M-%S"
current_directory = os.path.dirname(os.path.abspath(__file__))
db_connstring = os.getenv("HINTS_DB_CONNSTRING")


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "my secret key"

# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, "postgre_db"):
#         try:
#             g.postgre_db = psycopg2.connect(db_connstring)
#         except psycopg2.Error as e:
#             raise Exception("DB connection error")  # reraise to hide internals
#     return g.postgre_db

db = psycopg2.connect(db_connstring)


@app.errorhandler(Exception)
def general_error(e):
    logging.exception("Programmer error: %s, url: %s", e, request.url)
    return "Server error <!--{}({})-->".format(type(e).__name__, e), 500


@app.errorhandler(jinja2.exceptions.UndefinedError)
def template_error(e):
    logging.exception("Template error: %s, url: %s", e, request.url)
    return "Server error", 500


@app.errorhandler(404)
def error_404(e):
    logging.exception("Error: %s, url: %s", e, request.url)
    return "Error 404", 404


@app.errorhandler(500)
def error_500(e):
    logging.exception("Error: %s, url: %s", e, request.url)
    return "Error 500", 500


@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        if value is None and key in args:
            del args[key]
        else:
            args[key] = value

    return "?" + format(url_encode(args)) if args else ""


def validation_error_handler(err, data, main_def):
    abort(jsonify({"error": str(err)}, 400))


# class Vacancy(db.Model):
#     __tablename__ = "vacancies"
#     vacancy_id = db.Column(db.Integer(), primary_key=True)
#     vacancy_name = db.Column(db.String())
#     profession = db.Column(db.String())
#     industry = db.Column(db.String())
#     experience = db.Column(db.String())
#     key_skills = db.Column(db.String())
#     employer = db.Column(db.String())
#     area = db.Column(db.String())
#     salary_from = db.Column(db.Integer())
#     salary_to = db.Column(db.Integer())
#     currency = db.Column(db.String())
#     published_at = db.Column(db.DateTime())
#     created_at = db.Column(db.DateTime())
#     archived = db.Column(db.Boolean()) #add date when archived
#     schedule = db.Column(db.String())
#     url = db.Column(db.String())
# description

# create all
# from app import app, db
# app.app_context().push()
# db.create_all()


@app.route("/")
def hello():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
