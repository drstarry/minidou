#!/usr/bin/python
# coding: utf-8
from setuptools import setup, find_packages

install_requires = [
    'bottle',
    'click',
    'jieba',
    'json',
    'logging',
    'os',
    'panda',
    'string',
    'sys',
    'time',
    'urllib',
    'urllib2',
]

entry_points = {'console_scripts': ['run_server = minidou.api:run_server']}

setup(name='minidou',
      version='0.0.1',
      author='Rui Dai | Starry',
      author_email='drstarry@gmail.com',
      description='minidou',
      license='PRIVATE',
      packages=find_packages(),
      install_requires=install_requires,
      entry_points=entry_points)
