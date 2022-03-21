from flask import Flask, render_template, render_template_string, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


current_directory = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://hints:password@localhost/hints?connect_timeout=5"
app.config["SECRET_KEY"] = "my secret key"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Vacancies(db.Model):
    __tablename__ = "vacancies"
    id = db.Column(db.Integer, primary_key=True)
    vacancy_name = db.Column(db.String())
    employer = db.Column(db.String())
    area = db.Column(db.String())
    salary_from = db.Column(db.Integer())
    salary_to = db.Column(db.Integer())
    currency = db.Column(db.String())
    published_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime())
    archived = db.Column(db.DateTime())
    schedule = db.Column(db.String())
    url = db.Column(db.String())


class TestTable(db.Model):
    __tablename__ = "testtable"
    id = db.Column(db.Integer, primary_key=True)
    vacancy_name = db.Column(db.String())


# export $(grep -v '^#' .env | xargs)
from app import app, db, TestTable
app.app_context().push()
db.create_all()


@app.route("/")
def hello():
    return {"hello": "world"}


if __name__ == "__main__":
    app.run(debug=True)
