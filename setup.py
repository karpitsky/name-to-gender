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
    author='Michael Karpitsky',
    author_email='michael.karpitsky@gmail.com',
    license='BSD',
    install_requires=['six'],
    url='https://github.com/karpitsky/name-to-gender',
    keywords=['Gender', 'Python'],
    packages=['nametogender'],
    package_data={'nametogender': ['names.pickle']},
)
