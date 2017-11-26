#!/usr/bin/env bash

#
# run pytext on travis in a own virtualenv
#

# exits on fail
set -e

# creates & uses the virtualenv
virtualenv --python=python2.7 --no-site-packages venv
source venv/bin/activate

cython=$(grep Cython requirements/base.txt)
if [ "${cython}" == "" ]; then
    echo -e "\nERROR getting cython install string!"
    exit -1
fi

# installs requirements
pip install --install-option="--no-cython-compile" ${cython}
pip install -r requirements/dev.txt

# runs tests
pytest
