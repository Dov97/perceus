# File Name   : run.sh
# Description : Singular run file for the Perceus Technologies take home
#               assignment. Both Linux and Mac supported.
# Github Repo : https://github.com/Dov97/perceus
# Author      : David Sellars
# Email       : dovsellars@gmail.com

# Default - used for M1 Mac development.
#!/opt/homebrew/bin/bash

# Use for Linux and Intel Mac development
# #!/bin/bash


# Setup Flask enviroment.
export FLASK_APP=application.py

# Global varbiles.
python_path=$(which python3)
app="application.py"

# Display the help information.
Help()
{
    usage='Usage: ./run.sh <option>

OPTIONS
    app                 Run application.py.
    code_audit          Run pylama linters; pyflakes, pylint, radon.
    doc_audit           Run pydocstyl linter.
    unit_tests          Run pytest unit tests.
    gen_api_doc         Run pdoc generating API documentation.

EXIT STATUS
  0  Success.
'
    printf '%s\n' "${usage}"
}

# Remove cache files.
find . -type d -name "__pycache__" | xargs rm -rf

# Handle the command line arguments with a simple switch/case statement.
case "${1}" in
    "app")
        # Use ./services/dev_data.db.
        export FLASK_ENV=development
        "${python_path}" "${app}"
        return_code="${PIPESTATUS[0]}"
        ;;
    "code_audit")
        pylama --verbose --options ./setup.cfg "${app}"
        return_code="${PIPESTATUS[0]}"
        ;;
    "doc_audit")
        pydocstyle --ignore D105,D213,D203 "./${app}"
        return_code="${PIPESTATUS[0]}"
        ;;
    "unit_tests")
        # Use ./services/test_data.db, designed to be over written by tests.
        export FLASK_ENV=testing
        pytest -vs ./unit_tests
        return_code="${PIPESTATUS[0]}"
        ;;
    "gen_api_doc")
        pdoc ./application.py
        return_code="${PIPESTATUS[0]}"
        ;;
    *)
        Help
        exit 0
        ;;
esac

# Print the return code of the program run by the switch/case statement.
printf 'exit status: %s : %s\n'                                               \
       "${return_code}"                                                       \
       "${exit_status[${return_code}]}"

if [ "${return_code}" -eq 0 ]
then
    printf '*** NO ISSUES ***\n\n'
else
    printf '*** ISSUES FOUND ***\n\n'
fi

exit "${return_code}"
