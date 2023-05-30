"""application.py.

This script initialises a Flask application to manage users in a database.

The application uses SQLAlchemy for handeling the database and SQLite for the database system.

The Flask application provides the following functionalities:
- Create a user with a given first name, last name, email, and phone number.
- Get all users, a user by ID, a user by name.
- Delete a user by ID.
- Update a user email or phone number by ID.

Endpoints:
    Run ./run.sh gen_api_doc to generate endpoint documentation. Refer to README.md.

Author      : David Sellars
Email       : dovsellars@gmail.com
Github Repo : https://github.com/Dov97/perceus

"""


import os
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists


"""Initialise Flask app and select database depending on FLASK_ENV.

Development database : dev_data.db
Unit testing database: test_data.db

FLASK_ENV is automatically handled when running from run.sh but can be manually exported via shell.
"""
app = Flask(__name__)
dbName = None

if os.getenv("FLASK_ENV") == "testing":
    dbName = "test_data.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbName
else:
    dbName = "dev_data.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbName

db = SQLAlchemy(app)


class Email(db.Model):
    """Email class containing Id, mail and userID table columns.

    userID uses a foreign key to link emails to a specific user.
    This class has a child relationship to User().

    Parameters
    ----------
    db.Model : SQLAlchemy()
        Maps Email class to a database table.

    """

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        # Object output formatting.
        return f"{'userId': {self.userId}, 'Email': {self.id} - {self.mail}}"


class PhoneNumber(db.Model):
    """Phone number class containing Id, number and userID table columns.

    userID uses a foreign key to link phone number to a specific user.
    This class has a child relationship to User().

    Parameters
    ----------
    db.Model : SQLAlchemy()
        Maps PhoneNumber class to a database table.

    """

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(13), unique=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        # Object output formatting.
        return f"{self.id} - {self.number}"


class User(db.Model):
    """User class containing Id, number table columns with parent relationships to Email and PhoneNumber.

    Parameters
    ----------
    db.Model : SQLAlchemy()
        Maps User class to a database table.

    """

    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(30), nullable=False)
    firstName = db.Column(db.String(30), nullable=False)

    emails = db.relationship(Email, cascade="all,delete", backref='user', lazy=True)
    phoneNumbers = db.relationship(PhoneNumber, cascade="all,delete", backref='user', lazy=True)

    def __repr__(self):
        # Object output formatting.
        return (f"User({self.lastName} {self.firstName},Email: {self.emails},"
                f"Phone Number: {self.phoneNumbers})")


"""Create database if one does not exist already.

The database created will depend on FLASK_APP (hence dbName). Refer to flask initialisation section.
"""
if database_exists('sqlite:///instance/' + dbName):
    print(dbName + " already exists")
else:
    print(dbName + " does not exist, will create " + dbName)

    with app.app_context():
        try:
            db.create_all()
        except Exception as exception:
            print("Exception when attempting db.create_all(): " + str(exception))


@app.route('/')
def index():
    """Root / index route for application status.

    Returns
    -------
    Test string : String.

    """
    return 'Hello Perceus!'


@app.route('/users/', methods=["POST"])
def addUser():
    """Add a user to database as POST.

    Returns
    -------
    user ID (201, created) : String

    """
    user = User(
        lastName=request.json['lastName'],
        firstName=request.json['firstName'],
        emails=[Email(mail=email) for email in request.json.get('emails', [])],
        phoneNumbers=[PhoneNumber(number=number) for number in request.json.get('phoneNumbers', [])]
    )

    db.session.add(user)
    db.session.commit()

    return {'User added': user.id}, 201


@app.route('/users/')
def getUsers():
    """Get all users in the database.

    Returns
    -------
    All users (200, ok) : String

    """
    users = User.query.all()

    userDict = []
    for user in users:
        userDict.append({"lastName": user.lastName,
                         "firstName": user.firstName,
                         "emails": [email.mail for email in user.emails],
                         'phoneNumbers': [phone.number for phone in user.phoneNumbers]})

    return {"users": userDict}, 200


@app.route('/users/<int:id>')
def getUserById(id):
    """Get a user from database with the users ID.

    Parameters
    ----------
    id : Int
        user ID from route rule.

    Returns
    -------
    user (200, ok) : String

    Raise
    -----
    NotFound
        If the user with the given ID is not found.

    """
    user = db.session.get(User, id)
    if user is None:
        abort(404)

    userInfo = {"lastName": user.lastName,
                "firstName": user.firstName,
                "emails": [email.mail for email in user.emails],
                'phoneNumbers': [phone.number for phone in user.phoneNumbers]}

    return {"user": userInfo}, 200


@app.route('/users/<string:lastName>/<string:firstName>')
def getUserByName(firstName, lastName):
    """Get a user from database using last then first name.

    Parameters
    ----------
    lastName : String
        user last name from route rule.
    firstName : String
        user first name from route rule.

    Returns
    -------
    user (200, ok) : String

    """
    userFilterByLastName = User.query.filter_by(lastName=lastName).first()
    user = userFilterByLastName.query.filter_by(firstName=firstName).first()

    userInfo = {"lastName": user.lastName,
                "firstName": user.firstName,
                "emails": [email.mail for email in user.emails],
                'phoneNumbers': [phone.number for phone in user.phoneNumbers]}

    return {"user": userInfo}, 200


@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
    """Delete a user from database with the users ID.

    Parameters
    ----------
    id : Int
        user ID from route rule.

    Returns
    -------
    user ID (200, ok) : String

    Raise
    -----
    NotFound
        If the user with the given ID is not found.

    """
    user = db.session.get(User, id)
    if user is None:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    return {'User deleted': id}, 200


@app.route('/users/<int:id>/add_email', methods=['POST'])
def addUserEmail(id):
    """Add a user email to database with POST using the ID.

    Parameters
    ----------
    id : Int
        user ID from route rule.

    Returns
    -------
    user email (201, created) : String

    Raise
    -----
    NotFound
        If the user with the given ID is not found.

    """
    user = db.session.get(User, id)
    if user is None:
        abort(404)

    newEmail = [Email(mail=email) for email in request.json.get('emails', [])]

    user.emails.extend(newEmail)
    db.session.commit()

    return {'Email added': [email.mail for email in newEmail]}, 201


@app.route('/users/<int:id>/add_phone_number', methods=['POST'])
def addPhoneNumber(id):
    """Add a user phone number to database with POST using the ID.

    Parameters
    ----------
    id : Int
        user ID from route rule.

    Returns
    -------
    user phone number (201, created) : String

    Raise
    -----
    NotFound
        If the user with the given ID is not found.


    """
    user = db.session.get(User, id)
    if user is None:
        abort(404)

    newNumber = [PhoneNumber(number=phone_number) for phone_number in request.json.get('phoneNumbers', [])]

    user.phoneNumbers.extend(newNumber)
    db.session.commit()

    return {'Number added': [phone.number for phone in newNumber]}, 201


@app.route('/users/<int:id>/update_email/<int:email_id>', methods=['POST'])
def updateEmail(id, email_id):
    """Update a user email from the users ID in the database with POST.

    Parameters
    ----------
    id : Int
        user ID from route rule.
    email_id : Int
        email ID from route rule.

    Returns
    -------
    newEmail : String

    Raise
    -----
    NotFound
        If the user with the given ID is not found.

    """
    user = db.session.get(User, id)
    if user is None:
        abort(404)

    newEmail = request.json.get('emails')

    if email_id < len(user.emails):
        user.emails[email_id].mail = newEmail
    else:
        user.emails.append(Email(mail=newEmail))
        db.session.commit()

    return {'Email updated': newEmail}


@app.route('/users/<int:id>/update_number/<int:number_id>', methods=['POST'])
def updatePhoneNumber(id, numberId):
    """Update a users phone number from the user's ID in the database with POST.

    Parameters
    ----------
    id : Int
        user ID from route rule.
    numberId : Int
        phone number ID from route rule.

    Returns
    -------
    newNumber : String

    Raise
    -----
    NotFound
        If the user with the given ID is not found.

    """
    user = db.session.get(User, id)
    if user is None:
        abort(404)

    newNumber = request.json.get('phoneNumber')

    if numberId < len(user.phoneNumber):
        user.phoneNumber[numberId].number = newNumber
    else:
        user.phoneNumber.append(PhoneNumber(number=newNumber))
        db.session.commit()

    return {'Phone number updated': newNumber}


if __name__ == '__main__':
    app.run(port=8000)
