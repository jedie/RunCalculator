#!/usr/bin/env python
import io
import re

import os
from setuptools import setup, find_packages
import sys


PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


def read(*args):
    return open(os.path.join(PACKAGE_ROOT, *args)).read()

try:
    exec(read('run_calculator', 'version.py'))
except Exception as err:
    print("ERROR: %s" % err)
    __version__ = None


#_____________________________________________________________________________
# convert creole to ReSt on-the-fly, see also:
# https://github.com/jedie/python-creole/wiki/Use-In-Setup
long_description = None
for arg in ("test", "check", "register", "sdist", "--long-description"):
    if arg in sys.argv:
        try:
            from creole.setup_utils import get_long_description
        except ImportError as err:
            raise ImportError("%s - Please install python-creole - e.g.: pip install python-creole" % err)
        else:
            long_description = get_long_description(PACKAGE_ROOT)
        break
#----------------------------------------------------------------------------


setup(
    name='run_calculator',
    version=__version__,
    description='convert distance/time/pace for runners',
    long_description=long_description,
    author='Jens Diemer',
    author_email='run_calculator@jensdiemer.de',
    license='GNU General Public License v3 or later (GPLv3+)',
    packages=find_packages(
        exclude=[
            'docs', 'tests',
            'windows', 'macOS', 'linux',
            'iOS', 'android',
            'django'
        ]
    ),
    classifiers=[# https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    install_requires=[
    ],
    options={
        'app': {
            'formal_name': 'Run Calculator',
            'bundle': 'org.pybee.jensdiemer'
        },

        # Desktop/laptop deployments
        'macos': {
            'app_requires': [
                'toga-cocoa',
            ]
        },
        'linux': {
            'app_requires': [
                'toga-gtk',
            ]
        },
        'windows': {
            'app_requires': [
                'toga-winforms',
            ]
        },

        # Mobile deployments
        'ios': {
            'app_requires': [
                'toga-ios',
            ]
        },
        'android': {
            'app_requires': [
                'toga-android',
            ]
        },

        # Web deployments
        'django': {
            'app_requires': [
                'toga-django',
            ]
        },
    }
)
