"""application.py.

File Info   : Main application file for the Perceus Technologies take home
              assignment.
Github Repo : https://github.com/Dov97/perceus
Author      : David Sellars
Email       : dovsellars@gmail.com
"""

import os
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists

""" Initialise App and Database. """
app = Flask(__name__)

"""
Select development or testing database depending on FLASK_ENV.
This is automatically handled when running from run.sh but can be manually
exported via shell.
"""
dbName = None

if os.getenv("FLASK_ENV") == "testing":
    dbName = "test_data.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbName
else:
    dbName = "dev_data.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbName

db = SQLAlchemy(app)


""" Classes """
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    # Column linked to to user ID - critical for link to User.
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        # Object output formatting.
        return f"{'userId': {self.userId}, 'Email': {self.id} - {self.mail}}"


class PhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(13), unique=True, nullable=False)
    # Column linked to to user ID - critical for link to User.
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        # Object output formatting.
        return f"{self.id} - {self.number}"


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(30), nullable=False)
    firstName = db.Column(db.String(30), nullable=False)

    # Class relationships (parent/child).
    emails = db.relationship(Email, cascade="all,delete", backref='user', lazy=True)
    phoneNumbers = db.relationship(PhoneNumber, cascade="all,delete", backref='user', lazy=True)

    def __repr__(self):
        return (f"User({self.lastName} {self.firstName},Email: {self.emails},"
                f"Phone Number: {self.phoneNumbers})")


""" Create database if one does not exist already. """
if database_exists('sqlite:///instance/'+ dbName):
    print(dbName + " already exists")
else:
    print(dbName + " does not exist, will create " + dbName)
    # this is needed in order for database session calls to create and commit.
    with app.app_context():
        try:
            db.create_all()
        except Exception as exception:
            print("got the following exception when attempting db.create_all(): " + str(exception))




if __name__ == '__main__':
    app.run(port=8000)