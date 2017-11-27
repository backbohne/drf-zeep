#!/usr/bin/env python

import os
import re

from setuptools import find_packages, setup
from pip.req import parse_requirements
from pip.download import PipSession
from collections import defaultdict

def text_of(relpath):
    thisdir = os.path.dirname(__file__)
    file_path = os.path.join(thisdir, os.path.normpath(relpath))
    with open(file_path) as f:
        text = f.read()
    return text


NAME = 'drf-zeep'
VERSION = '1.0'
DESCRIPTION = 'Zeep WSDL/XSD type to Django Restframework converter.'
LONG_DESCRIPTION = DESCRIPTION
KEYWORDS = 'soap zeep django restframework'
AUTHOR = 'Frank Bohnsack'
AUTHOR_EMAIL = 'frank.bohnsack@iway.ch'
URL = 'https://github.com/backbohne/drf-zeep'
LICENSE = text_of('LICENSE.txt')
PACKAGES = find_packages(exclude=['tests', 'tests.*'])
DEPENDENCY_LINKS = []
INSTALL_REQUIRES = []
EXTRAS_REQUIRES = defaultdict(list)
for r in parse_requirements('requirements.txt', session='hack'):
    if r.link:
        DEPENDENCY_LINKS.append(str(r.link))
    elif r.markers:
        EXTRAS_REQUIRES[':' + str(r.markers)].append(str(r.req))
    else:
        INSTALL_REQUIRES.append(str(r.req))
TEST_SUITE = 'tests'
TESTS_REQUIRE = []
CLASSIFIERS = [
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries',
]

params = {
    'name':                 NAME,
    'version':              VERSION,
    'description':          DESCRIPTION,
    'keywords':             KEYWORDS,
    'long_description':     LONG_DESCRIPTION,
    'author':               AUTHOR,
    'author_email':         AUTHOR_EMAIL,
    'url':                  URL,
    'license':              LICENSE,
    'packages':             PACKAGES,
    'include_package_data': True,
    'install_requires':     INSTALL_REQUIRES,
    'extras_require':       EXTRAS_REQUIRES,
    'dependency_links':     DEPENDENCY_LINKS,
    'tests_require':        TESTS_REQUIRE,
    'test_suite':           TEST_SUITE,
    'classifiers':          CLASSIFIERS,
}

setup(**params)
