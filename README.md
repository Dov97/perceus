# README.md
File Info   : Usage and API.
Github Repo : https://github.com/Dov97/perceus
Author      : David Sellars
Email       : dovsellars@gmail.com


Task:

    Repo: https://github.com/perseusEngineering/candidate-coding-challenges/tree/master/backend-challenges/user-service


Solution:

    Repo: https://github.com/Dov97/perceus


Files and FS Structure:

    .
    ├── README.md --------------- This file.
    ├── application.py ---------- Main application run via run.sh.
    ├── instance
    │   ├── dev_data.db --------- Dev sqlite DB for application runs (creation handled).
    │   └── test_data.db -------- Test sqlite DB for unit test runs (creation handled).
    ├── requirements.txt -------- Pip3 requirements.
    ├── run.sh ------------------ Singular run script for all opporations.
    ├── setup.cfg --------------- Pylama configuration (code formatting).
    └── unit_tests
        ├── __init__.py
        └── test_application.py - Unit tests for application.py.


Prerequisites:

    1.  Mac or Linux shell.
    2.  Git.
    3.  Python 3.11.3 installed and on system PATH.
    4.  Pip3 installed via Python.


Setup:

    1.  Create a python venv to isolate Python from system Python:
            python3 -m venv .venv

    2.  Activate the venv:
            source ./.venv//bin/activate

    3.  Run the following to install all pip requirements:
            pip3 install -r ./requirements.txt

    4.  Enable the correct system shbang in run.sh (#!)
        M1 Mac is by default, Intel Mac and Linux can be enabled.
        Windows users refer to "Usage" to run with out run.sh.


Usage:

    Run.sh is provided as a single run point for all opporations. To run a
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

