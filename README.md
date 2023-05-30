# README.md
File Info   : Usage and API.
Github Repo : https://github.com/Dov97/perceus
Author      : David Sellars
Email       : dovsellars@gmail.com


Task:

    Repo: https://github.com/perseusEngineering/candidate-coding-challenges/tree/master/backend-challenges/user-service


Files and FS Structure:

    .
    ├── README.md --------------- This file.
    ├── application.py ---------- Main application run via run.sh.
    ├── instance ---------------- Folder generated with dev or test database on app or unit_tests runs.
    ├── requirements.txt -------- Pip3 requirements to install.
    ├── run.sh ------------------ Singular run script for all operations.
    ├── setup.cfg --------------- Pylama configuration (code formatting).
    └── unit_tests
        ├── __init__.py
        └── test_application.py - Unit tests for application.py.


Prerequisites:

    1.  Bash shell, see "Usage" for how to run operations without run.sh.
    2.  Git.
    3.  Python 3.11.3 installed and on system PATH.
    4.  Pip3 installed via Python.


Setup:

    1.  Clone the solution repo if not already done:
            git clone https://github.com/Dov97/perceus.git

    2.  Cd into ./perceus and create a python venv to isolate Python from system Python:
            cd ./perceus && python3 -m venv .venv

    3.  Activate the venv:
            source ./.venv/bin/activate

    4.  Upgrade pip:
            pip install --upgrade pip

    5.  Install all pip requirements:
            pip3 install -r ./requirements.txt


Usage:

    Run.sh is provided as a single run point for all operations. To run a
    opporation follow the run.sh usage (help):

        Usage: ./run.sh <option>

        OPTIONS
            app                 Run application.py.
            code_audit          Run pycodestyle, pyflakes, pylint and radon via pylama.
            doc_audit           Run pydocstyle.
            unit_tests          Run pytest unit tests.
            gen_api_doc         Run pdoc generating API documentation.

        EXIT STATUS
          0  Success.

    To run without run.sh use the following commands:

        app:

            export FLASK_ENV=development
            python3 ./application.py

            Where the export sets the Flask environment, setting the database used
            to dev_data.db.

        code_audit:

            pylama --verbose --options ./setup.cfg ./application.py

        doc_audit:

            pydocstyle --ignore D105,D213,D203 "./application.py

        unit_tests:

            export FLASK_ENV=testing
            pytest -vs ./unit_tests

            Where the export sets the Flask environment, setting the database used
            to test_data.db.

        gen_api_doc:

            pdoc ./application.py

