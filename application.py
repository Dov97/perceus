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


""" Routes """
@app.route('/')
def index():

    return 'Hello Perceus!'


@app.route('/users', methods=["POST"])
def addUser():

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

    users = User.query.all()

    userDict = []
    for user in users:
        userDict.append({"lastName": user.lastName,
                         "firstName": user.firstName,
                         "emails": [email.mail for email in user.emails],
                         'phoneNumbers': [phone.number for phone in user.phoneNumbers]})

    return {"users" : userDict}


@app.route('/users/<int:id>')
def getUserById(id):

    user = db.session.get(User, id)
    if user is None:
        abort(404)

    userInfo = {"lastName": user.lastName,
                "firstName": user.firstName,
                "emails": [email.mail for email in user.emails],
                'phoneNumbers': [phone.number for phone in user.phoneNumbers]}

    return {"user" : userInfo}


@app.route('/users/<string:firstName>/<string:lastName>')
def getUserByName(firstName, lastName):

    userFilterByLast = User.query.filter_by(lastName=lastName).first()
    user = userFilterByLast.query.filter_by(firstName=firstName).first()

    userInfo = {"lastName": user.lastName,
                "firstName": user.firstName,
                "emails": [email.mail for email in user.emails],
                'phoneNumbers': [phone.number for phone in user.phoneNumbers]}

    return {"user" : userInfo}


@app.route('/users/<int:id>', methods=['DELETE'])
def deleteUser(id):
    user = db.session.get(User, id)
    if user is None:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    return {'message': f'Deleted user with id: {id}'}, 200


@app.route('/users/<int:id>/add_email', methods=['POST'])
def addUserEmail(id):

    user = db.session.get(User, id)
    if user is None:
        abort(404)

    new_email = [Email(mail=email) for email in request.json.get('emails', [])]

    user.emails.extend(new_email)
    db.session.commit()

    return {'Email added': [email.mail for email in new_email]}, 201


@app.route('/users/<int:id>/add_phone_number', methods=['POST'])
def addPhoneNumber(id):

    user = db.session.get(User, id)
    if user is None:
        abort(404)

    new_number = [PhoneNumber(number=phone_number) for phone_number in request.json.get('phoneNumbers', [])]

    user.phoneNumbers.extend(new_number)
    db.session.commit()

    return {'Number added': [phone.number for phone in new_number]}, 201


@app.route('/users/<int:id>/update_email/<int:email_id>', methods=['POST'])
def updateEmail(id, email_id):

    user = User.query.get(id)
    if user is None:
        abort(404)

    # Create new email.
    new_email = request.json.get('emails')

    # Assume that a user can have only one email.
    if email_id < len(user.emails):
        user.emails[email_id].mail = new_email
    else:
        user.emails.append(Email(mail=new_email))
        db.session.commit()

    return {'Email updated' : new_email}


if __name__ == '__main__':
    app.run(port=8000)