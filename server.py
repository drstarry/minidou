#!env python2
#encoding: utf8

import sys
import os
import os.path
from bottle import route, run, template, view, static_file, request, urlencode, redirect

#import sample_data
import time
import json


@route('/')
def index():
    return template('index')

@route('/about')
def index():
    return template('about')

@route('/static/<path:path>')
def static(path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    return static_file(path, root=curdir + '/static/')

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 8081

run(server='auto', host='0.0.0.0', port=port, reloader=True, debug=True)
