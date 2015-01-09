#!/usr/bin/python
# coding: utf-8

import os

PORT = 8080


"""
path config
"""
def get_project_root_dir():
    import minidou
    return os.path.abspath(os.path.dirname(os.path.dirname(minidou.__file__)))

ROOT_PATH = get_project_root_dir() + '/minidou'
TEMPLATE_PATH = ROOT_PATH + '/view'
STATIC_PATH = ROOT_PATH + '/static'


"""
response status config
"""
NORMAL_STATUS = 1
BAD_STATUS = 0
