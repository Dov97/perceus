"""application.py.

File Info   : Main application file for the Perceus Technologies take home
              assignment.
Github Repo : https://github.com/Dov97/perceus
Author      : David Sellars
Email       : dovsellars@gmail.com
"""

import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


# Initialise environment.
app = Flask(__name__)
app.app_context().push()

# Select development or testing database depending on FLASK_ENV (see run.sh).
if os.getenv("FLASK_ENV") == "testing":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_data.db"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev_data.db"

db = SQLAlchemy(app)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    # ForeignKey uses user.id for key.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.mail}"


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(13), unique=True, nullable=False)
    # ForeignKey uses user.id for key.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.number}"


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(30), nullable=False)
    firstName = db.Column(db.String(30), nullable=False)

    # Class relationships (parent/child).
    emails = db.relationship(Email, db.ForeignKey('user.id'), backref='user', lazy=True)
    PhoneNumber = db.relationship(PhoneNumber, db.ForeignKey('user.id'), backref='user', lazy=True)

    def __repr__(self):
        return (f"User({self.lastName} {self.firstName},Email: {self.emails},"
                f"Phone Number: {self.PhoneNumber})")


if __name__ == '__main__':
    app.run(port=8000)
