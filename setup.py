#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.0.7'

setup(
    name='nametogender',
    version=VERSION,
    description='Name to gender library for python',
    author='Michael K,
    license='BSD',
    install_requires=[],
    url='https://github.com/karpitsky/name-to-gender',
    keywords=['Gender', 'Python'],
    packages=['nametogender'],
    package_data={'nametogender': ['names.csv', 'data/*']},
)
