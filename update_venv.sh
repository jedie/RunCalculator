#!/usr/bin/env bash

set -e

(
    set -x
    cd ${VIRTUAL_ENV}

    pip3 install --upgrade pip

    cd ${VIRTUAL_ENV}/src/toga
    git pull
    pip install -e src/core
    pip install -e src/dummy
    pip install -e src/gtk
    pip install -e src/django

    cd ${VIRTUAL_ENV}/src/run-calculator
    git pull
    pip install -e .

    cd ${VIRTUAL_ENV}/src/briefcase
    git pull
    pip install -e .

    pip freeze
)
