#!/usr/bin/env python
import io
import re

import os
from setuptools import setup, find_packages
import sys


PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


with io.open('./run_calculator/__init__.py', encoding='utf8') as version_file:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")


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
    version=version,
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
    classifiers=[
        'Development Status :: 1 - Planning',
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
                'toga-cocoa==0.3.0.dev7',
            ]
        },
        'linux': {
            'app_requires': [
                'toga-gtk==0.3.0.dev7',
            ]
        },
        'windows': {
            'app_requires': [
                'toga-winforms==0.3.0.dev7',
            ]
        },

        # Mobile deployments
        'ios': {
            'app_requires': [
                'toga-ios==0.3.0.dev7',
            ]
        },
        'android': {
            'app_requires': [
                'toga-android==0.3.0.dev7',
            ]
        },

        # Web deployments
        'django': {
            'app_requires': [
                'toga-django==0.3.0.dev7',
            ]
        },
    }
)
