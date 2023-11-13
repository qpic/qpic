#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import sys
if sys.version_info[:2] >= (3,0):
    openargs = {'encoding':'utf-8'}
else:
    openargs = {}

with open('README.rst','r',**openargs) as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst','r',**openargs) as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='qpic',
    version='1.1.0',
    description="Creating quantum circuit diagrams in TikZ",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    author="Sandy Kutin, Thomas Draper",
    author_email='kutin@idaccr.org, tdraper@ccr-lajolla.org',
    url='https://github.com/qpic/qpic',
    packages=[
        'qpic',
    ],
    package_dir={'qpic':
                 'qpic'},
    scripts=['bin/qpic', 'bin/tikz2preview'],
    include_package_data=True,
    install_requires=requirements,
    license="GPL",
    zip_safe=False,
    keywords='qpic',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
