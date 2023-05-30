"""test_application.py.

File Info   : Unit test the application
Author      : David Sellars
Email       : dovsellars@gmail.com
Github Repo : https://github.com/Dov97/perceus
"""

import os
import pytest
from application import app, db, User, Email, PhoneNumber


"""Fixture methods."""

@pytest.fixture
def client():
    """
    Configure Flask app to testing so asserts and exceptions run.
    Run a test client, yield to run tests.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def initDatabase():
    """Initialise database and FLASK_ENV."""
    if os.getenv("FLASK_ENV") != "testing":
        raise ValueError("Cannot run tests when FLASK_ENV != \"testing\"")

    with app.app_context():
        try:
            db.create_all()
        except Exception as exception:
            print("Exception when attempting db.create_all(): " + str(exception))

        # Yield to run tests.
        yield db

        # Drop sqlite tables.
        db.drop_all()


@pytest.fixture
def newUser():
    """Create new user object and return user instance."""
    user = User(
                    lastName="McTesty",
                    firstName="Tester",
                    emails=[Email(mail="testermctesty@gmail.com")],
                    phoneNumbers=[PhoneNumber(number="441234567890")]
    )

    return user


@pytest.fixture
def newEmail():
    """Create new email and return email instance."""
    email = Email(mail="newtestemail@gmail.com")

    return email


@pytest.fixture
def newPhoneNumber():
    """Create new phone number and return phoneNumber instance."""
    phoneNumber = PhoneNumber(number="440987654321")

    return phoneNumber


"""Test methods."""

def test_index(client):
    """Get index and assert."""

    response = client.get('/')
    assert response.data == b'Hello Perceus!'


def test_add_user(client, initDatabase, newUser):
    """Test adding a user."""

    response = client.post('/users/', json={
        'lastName': newUser.lastName,
        'firstName': newUser.firstName,
        'emails': [email.mail for email in newUser.emails],
        'phoneNumbers': [phoneNumber.number for phoneNumber in newUser.phoneNumbers]
    })

    assert response.status_code == 201
    assert response.get_json()['user_id'] == 1


def test_get_users(client, initDatabase, newUser):
    """Test getting all users."""

    initDatabase.session.add(newUser)
    initDatabase.session.commit()

    response = client.get('/users/')

    assert response.get_json() is not None, "Response data is None."
    users = response.get_json().get('users')

    assert users is not None, "No users in response."
    assert response.status_code == 200
    assert users[0]['lastName'] == newUser.lastName
    assert users[0]['firstName'] == newUser.firstName


def test_get_user_by_id(client, initDatabase, newUser):
    """Test getting a user by id."""

    initDatabase.session.add(newUser)
    initDatabase.session.commit()

    response = client.get('/users/1')
    user = response.get_json()['user']

    assert response.status_code == 200
    assert user['lastName'] == newUser.lastName
    assert user['firstName'] == newUser.firstName


def test_get_user_by_name(client, initDatabase, newUser):
    """Test getting a user by name."""

    initDatabase.session.add(newUser)
    initDatabase.session.commit()

    response = client.get(f'/users/{newUser.lastName}/{newUser.firstName}')
    user = response.get_json()['user']

    assert response.status_code == 200
    assert user['lastName'] == newUser.lastName
    assert user['firstName'] == newUser.firstName


def test_delete_user(client, initDatabase, newUser):
    """Test deleting a user."""

    initDatabase.session.add(newUser)
    initDatabase.session.commit()

    response = client.delete('/users/1')

    assert response.status_code == 200
    assert response.get_json()['user_id'] == 1


def test_add_user_email(client, initDatabase, newUser, newEmail):
    """Test adding a user email."""

    initDatabase.session.add(newUser)
    initDatabase.session.commit()

    response = client.post('/users/1/add_email', json={
        'emails': [newEmail.mail]
    })

    assert response.status_code == 201
    assert response.get_json()['user_email'][0] == newEmail.mail


def test_add_user_phone_number(client, initDatabase, newUser, newPhoneNumber):
    """Test adding a user phone number."""

    initDatabase.session.add(newUser)
    initDatabase.session.commit()

    response = client.post('/users/1/add_phone_number', json={
        'phoneNumbers': [newPhoneNumber.number]
    })

    assert response.status_code == 201
    assert response.get_json()['user_number'][0] == newPhoneNumber.number


def test_update_user_email(client, initDatabase, newUser, newEmail):
    """Test updating a user email."""

    initDatabase.session.add(newUser)
    initDatabase.session.commit()

    response = client.post('/users/1/update_email/0', json={
        'emails': newEmail.mail
    })

    assert response.status_code == 200
    assert response.get_json()['user_email'] == newEmail.mail

def test_update_user_phone_number(client, initDatabase, newUser, newPhoneNumber):
    """Test updating a user phone number."""

    initDatabase.session.add(newUser)
    initDatabase.session.commit()

    response = client.post('/users/1/update_phone_number/0', json={
        'phoneNumbers': newPhoneNumber.number
    })

    assert response.status_code == 200
    assert response.get_json()['user_number'] == newPhoneNumber.number
