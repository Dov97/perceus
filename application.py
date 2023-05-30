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


"""
Select development or testing database depending on FLASK_ENV.
This is automatically handled when running from run.sh but can be manually
exported via shell.
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
    """Email class with db columns and a child relationship to User."""

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(50), unique=True, nullable=False)
    # Column linked to to user ID.
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        # Object output formatting.
        return f"{'userId': {self.userId}, 'Email': {self.id} - {self.mail}}"


class PhoneNumber(db.Model):
    """Phone number class with db columns and a child relationship to User."""

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(13), unique=True, nullable=False)
    # Column linked to to user ID.
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        # Object output formatting.
        return f"{self.id} - {self.number}"


class User(db.Model):
    """
    User class with db name columns and parent relationships for emails and
    phoneNumbers.
    """

    id = db.Column(db.Integer, primary_key=True)
    lastName = db.Column(db.String(30), nullable=False)
    firstName = db.Column(db.String(30), nullable=False)

    # Class relationships (parent/child).
    emails = db.relationship(Email, cascade="all,delete", backref='user', lazy=True)
    phoneNumbers = db.relationship(PhoneNumber, cascade="all,delete", backref='user', lazy=True)

    def __repr__(self):
        return (f"User({self.lastName} {self.firstName},Email: {self.emails},"
                f"Phone Number: {self.phoneNumbers})")


""" Create database if one does not exist already."""
if database_exists('sqlite:///instance/' + dbName):
    print(dbName + " already exists")
else:
    print(dbName + " does not exist, will create " + dbName)

    with app.app_context():
        try:
            db.create_all()
        except Exception as exception:
            print("got the following exception when attempting db.create_all(): " + str(exception))


@app.route('/')
def index():
    """Base route.

    Returns:
        (string): Test string.
    """

    return 'Hello Perceus!'


@app.route('/users', methods=["POST"])
def addUser():
    """Add a user to database with POST.

    Returns:
        user.id (int): User ID with a 201 code.
    """

    user = User(
        lastName=request.json['lastName'],
        firstName=request.json['firstName'],
        emails=[Email(mail=email) for email in request.json.get('emails', [])],
        phoneNumbers=[PhoneNumber(number=number) for number in request.json.get('phoneNumbers', [])]
    )

    db.session.add(user)
    db.session.commit()

    return {'id': user.id}, 201


@app.route('/users/')
def getUsers():
    """Get all users in the database.

    Returns:
        userDict (string): All users information.
    """

    users = User.query.all()

    userDict = []
    for user in users:
        userDict.append({"lastName": user.lastName,
                         "firstName": user.firstName,
                         "emails": [email.mail for email in user.emails],
                         'phoneNumbers': [phone.number for phone in user.phoneNumbers]})

    return {"users": userDict}


@app.route('/users/<int:id>')
def getUserById(id):
    """Get a user from database with the users ID.

    Parameters:
        id (int): User ID.

    Returns:
        userInfo (string): User information of route rule ID.
    """

    user = db.session.get(User, id)
    if user is None:
        abort(404)

    userInfo = {"lastName": user.lastName,
                "firstName": user.firstName,
                "emails": [email.mail for email in user.emails],
                'phoneNumbers': [phone.number for phone in user.phoneNumbers]}

    return {"user": userInfo}


@app.route('/users/<string:lastName>/<string:firstName>')
def getUserByName(firstName, lastName):
    """Get a user from database using last then first name.

    Parameters:
        firstName (string): Users first name from route rule.
        lastName (string): Users last name from route rule.

    Returns:
        userInfo (string): User information of route rule names.
    """

    userFilterByLast = User.query.filter_by(lastName=lastName).first()
    user = userFilterByLast.query.filter_by(firstName=firstName).first()

    userInfo = {"lastName": user.lastName,
                "firstName": user.firstName,
                "emails": [email.mail for email in user.emails],
                'phoneNumbers': [phone.number for phone in user.phoneNumbers]}

    return {"user": userInfo}


@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
    """Delete a user from database with the users ID.

    Parameters:
        id (int): User ID from route rule.

    Returns:
        id message (string): Deleted user ID with 200 response.
    """

    user = db.session.get(User, id)
    if user is None:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    return {'message': f'Deleted user with id: {id}'}, 200


@app.route('/users/<int:id>/add_email', methods=['POST'])
def addUserEmail(id):
    """Add a user email to database with POST using the users ID.

    Parameters:
        id (int): User ID from route rule.

    Returns:
        new_email (string): Email added with 201 response.
    """

    user = db.session.get(User, id)
    if user is None:
        abort(404)

    new_email = [Email(mail=email) for email in request.json.get('emails', [])]

    user.emails.extend(new_email)
    db.session.commit()

    return {'Email added': [email.mail for email in new_email]}, 201


@app.route('/users/<int:id>/add_phone_number', methods=['POST'])
def addPhoneNumber(id):
    """Add a user phone number to database with POST using the users ID.

    Parameters:
        id (int): User ID from route rule.

    Returns:
        new_number (string): Phone number added with 201 response.
    """

    user = db.session.get(User, id)
    if user is None:
        abort(404)

    new_number = [PhoneNumber(number=phone_number) for phone_number in request.json.get('phoneNumbers', [])]

    user.phoneNumbers.extend(new_number)
    db.session.commit()

    return {'Number added': [phone.number for phone in new_number]}, 201


@app.route('/users/<int:id>/update_email/<int:email_id>', methods=['POST'])
def updateEmail(id, email_id):
    """Update a user email from the users ID in the database with POST.

    Parameters:
        id (int): User ID from route rule.
        email_id (int): Email ID from route rule.

    Returns:
        new_email (string): Updated email.
    """

    user = User.query.get(id)
    if user is None:
        abort(404)

    new_email = request.json.get('emails')

    if email_id < len(user.emails):
        user.emails[email_id].mail = new_email
    else:
        user.emails.append(Email(mail=new_email))
        db.session.commit()

    return {'Email updated': new_email}


@app.route('/users/<int:id>/update_number/<int:number_id>', methods=['POST'])
def updatePhoneNumber(id, email_id):
    """Update a user phone number from the users ID in the database with POST.

    Parameters:
        id (int): User ID from route rule.
        email_id (int): phone number ID from route rule.

    Returns:
        new_number (string): Updated phone number.
    """

    user = User.query.get(id)
    if user is None:
        abort(404)

    new_email = request.json.get('emails')

    if email_id < len(user.emails):
        user.emails[email_id].mail = new_email
    else:
        user.emails.append(Email(mail=new_email))
        db.session.commit()

    return {'Email updated': new_email}


if __name__ == '__main__':
    app.run(port=8000)
