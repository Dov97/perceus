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

# Initialise environment.
app = Flask(__name__)
app.app_context().push()

# Select development or testing database depending on FLASK_ENV (see run.sh).
if os.getenv("FLASK_ENV") == "testing":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TESTING_DATABASE_URI")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DEVELOPMENT_DATABASE_URI")

db = SQLAlchemy(app)

# Roots and classes.

if __name__ == '__main__':
    app.run(port=8000)
