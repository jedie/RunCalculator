#!/usr/bin/env bash

#
# bootstrap file for:
#   https://github.com/jedie/RunCalculator
#
# see also:
#   https://toga.readthedocs.io/en/latest/how-to/contribute.html
#

set -e

DESTINATION=$(pwd)/RunCalculator-Env

(
    set -x
    python3 --version
    python3 -Im venv ${DESTINATION}
)
(
    cd ${DESTINATION}
    source bin/activate
    set -x
    pip3 install --upgrade pip


    mkdir -p src
    cd src
    git clone --depth=10 https://github.com/pybee/toga.git
    pip install -e toga/src/core
    pip install -e toga/src/dummy
    pip install -e toga/src/gtk

    pip3 install -e git+https://github.com/jedie/RunCalculator.git@pybee#egg=RunCalculator

    pip freeze
)
