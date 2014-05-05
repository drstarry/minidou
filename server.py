#!env python2.7
#encoding: utf8
import sys
import os
import os.path
import jieba
from bottle import route, run, template, view, static_file, request, urlencode, redirect
import time
import json
# sys.path('crawl')
# from weibocrawl import *

@route('/dou_friends')
def index():
    return template('dou_friends')

@route('/dou_events')
def index():
    return template('event')

@route('/crawl/<msg>', method='POST')
def crawl(msg):
    if msg == 'friends':
        pid = request.forms.get("id")
        degree = request.forms.get("degree")
        print pid,degree,span

        if pid and degree and span:
            print pid,degree,span
            f.write(str(pid)+" "+str(degree)+" "+str(span))

            redirect('/dou_events')
        redirect('/err/'+"您输入的信息不完整，请重新输入!")
    if msg == 'event':
        pid = request.forms.get("id")
        degree = request.forms.get("degree")
        print pid,degree,span

        if pid and degree and span:
            print pid,degree,span
            f.write(str(pid)+" "+str(degree)+" "+str(span))

            redirect('/dou_events')
        redirect('/err/'+"您输入的信息不完整，请重新输入!")
    redirect('/err/'+"您输入的信息不完整，请重新输入!")

@route('/map')
def index():
    return template('map.html')

@route('/analysis/<msg>')
def analysis(msg):
    return redirect(url_for('analysis.tpl', messages=msg))

@route('/vis/<msg>')
def analysis(msg):
    return redirect(url_for('visual.tpl', messages=msg))

@route('/upload_vis', method='POST')
def upload():
    # category = request.forms.get('category')
    file = request.files.file
    if file:
        name, ext = os.path.splitext(file.filename)
        if ext not in ('.txt','.dat','.csv'):
            return '格式错误，请您上传文本文件，后缀为.txt,.dat或者csv'
        curpath = os.getcwd()

        # save_path = get_save_path_for_category(category)
        file.save(curpath+"/static/upload_data") # appends upload.filename automatically
        msg = name+ext
        redirect('/analysis/'+msg)
    return "error!"

@route('/upload_ana', method='POST')
def upload():
    # category = request.forms.get('category')
    file = request.files.file
    if file:
        name, ext = os.path.splitext(file.filename)
        if ext not in ('.txt','.dat','.csv'):
            redirect('/err/'+"'格式错误，请您上传文本文件，后缀为.txt,.dat或者csv'")
        curpath = os.getcwd()

        # save_path = get_save_path_for_category(category)
        file.save(curpath+"/static/upload_data") # appends upload.filename automatically
        msg = name+ext
        redirect('/analysis/'+msg)
    redirect('/err/'+"您上传的文件有错误，请重试！")

@route('/err/<msg>')
@view('err')
def error(msg):
    return dict(
        err=msg
    )

@route('/vis')
def index():
    return template('visual')

@route('/')
def index():
    return template('index')

@route('/about')
def index():
    return template('about')

@route('/help')
def index():
    return template('help')

@route('/static/<path:path>')
def static(path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    return static_file(path, root=curdir + '/static/')

@route('/weibocrawl/<path:path>')
def static(path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    return static_file(path, root=curdir + '/weibocrawl/')

@route('/crawl/<path:path>')
def static(path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    return static_file(path, root=curdir + '/crawl/')

# @error('404')
# def error404(error):
#     return template('404')

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 8081

run(server='auto', host='0.0.0.0', port=port, reloader=True, debug=True)
