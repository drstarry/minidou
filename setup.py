#!/usr/bin/python
# coding: utf-8
from setuptools import setup

install_requires = [
    'bottle',
    'click',
    'jieba',
    'lxml',
    'pandas',
    'requests',
    'selenium'
]

entry_points = '''
[console_scripts]
minidou = minidou.cli.cli:cli
'''

setup(name='minidou',
      version='0.0.1',
      author='Rui Dai | Starry',
      author_email='drstarry@gmail.com',
      description='minidou',
      license='PRIVATE',
      include_package_data=True,
      zip_safe=False,
      packages=['minidou'],
      install_requires=install_requires,
      entry_points=entry_points
      )
