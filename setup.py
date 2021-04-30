# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='edgar',
    version='0.1.0',
    description='Downlad XBRL files from EDGAR',
    long_description=readme,
    author='Kenneth Reitz',
    author_email='flefebvre01@hotmail.com',
    url='https://github.com/FrankLef/edgar.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
