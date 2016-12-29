#!/usr/bin/env python                                                                                                                               
from setuptools import setup, find_packages


setup(
  name='sumatra python function runner',
  version='0.0.6',
  description='Runs function code based using code objects',
  author='Sumatra',
  packages=find_packages(),
  install_requires=[
    'six==1.10.0',
    'schematics==1.1.1'
  ],
  setup_requires=['pytest-runner'],
  tests_require=['pytest', 'pytest-sugar'],
  scripts=['bin/pyrunner']
)