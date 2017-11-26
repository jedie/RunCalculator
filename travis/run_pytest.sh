#!/bin/bash
# Linux specific Travis script

# exits on fail
set -e

# creates & uses the virtualenv
virtualenv --python=python2.7 --no-site-packages venv
source venv/bin/activate

# installs requirements
pip install --install-option="--no-cython-compile" $(grep Cython requirements.txt)
pip install -r requirements/dev.txt

# runs tests
pytest
