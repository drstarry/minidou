#!env python2.7
#encoding: utf8
import sys
import os
import os.path
import jieba
from bottle import route, run, template, view, static_file, request, urlencode, redirect ,error
import time
import json
from lib.crawl import DoubanCrawler
import json
import pandas as pd

@route('/movie')
def index():
    return template('movie')

@route('/event')
def index():
    return template('event')

@route('/crawl/<msg>', method='POST')
def crawl(msg):
    if msg == 'movie':
        pid = request.forms.get("id")
        degree = request.forms.get("degree")
        rtype = request.forms.get("rtype").split('.')[0]

        if pid and degree and rtype:
            print pid,degree,rtype
            seedurl = "http://movie.douban.com/subject/"+str(pid)
            crawl=DoubanCrawler(seedurl)
            coactor,movie = crawl.crawl_movie(degree)

            return template('m_info.tpl',movie=movie,coactor=coactor)
        return template('err.tpl',err="您输入的信息不完整，请重新输入!")

    if msg == 'event':
        print request.forms
        etype = request.forms.get("etype").split('.')[0]
        type_name = request.forms.get("etype").split('.')[1]
        etime = request.forms.get("etime").split('.')[0]
        time_name = request.forms.get("etime").split('.')[1]
        print etype,etime
        if etype and etime:
            etime_l = ["today","tomorrow","weekend","week"]
            etype_l = ["music","drama","salon","party","film","exhibition","sports","commomwheel","travel","all"]
            seedurl = "http://beijing.douban.com/events/"+str(etime_l[int(etime)-1])+"-"+str(etype_l[int(etype)-1])
            c=DoubanCrawler(seedurl)
            events = c.crawl_event()

            # data_to_js(events)
            return template('eventlist.tpl', events=events,etype=type_name,etime=time_name)
        return template('err.tpl',msg="您输入的信息不完整，请重新输入!")
    return template('err.tpl',msg="您输入的信息不完整，请重新输入!")

# def data_to_js(events):
#     f = open('static/vis_data/data.js','w')
#     # dis_list = [{'lat':39.902596,'lon':116.475052}{'lat':39.940605,'lon':116.436707}]
#     df = pd.DataFrame(events)
#     # print df
#     data =  df.groupby(['latitude','longtitude'])
#     print data
#     f.write('var data =[\n')
#     for e in df:
#         f.write('['+e['latitude'].encode('utf-8')+','+e['longtitude'].encode('utf-8')+',"'+e['title'].encode('utf-8')+'","'+e['loc'].encode('utf-8')+'","'+e['etime'].encode('utf-8')+'"],\n')
#     f.write('];\n')
#     return

@route('/map')
def map():
    return template('map.html')

@route('/eventlist')
def eve_list():
    return template('eventlist')

@route('/analysis/<msg>')
def analysis(msg):
    return redirect(url_for('analysis.tpl', messages=msg))

@route('/vis/<msg>')
def vis(msg):
    return redirect(url_for('visual.tpl', messages=msg))

@route('/upload_vis', method='POST')
def upload():
    # category = request.forms.get('category')
    file = request.files.file
    if file:
        name, ext = os.path.splitext(file.filename)
        if ext not in ('.txt','.dat','.csv'):
            return template('err.tpl',msg="格式错误，请您上传文本文件，后缀为.txt,.dat或者csv")
        curpath = os.getcwd()

        # save_path = get_save_path_for_category(category)
        file.save(curpath+"/static/upload_data") # appends upload.filename automatically
        msg = name+ext
        return template('visual.tpl',msg='')
    return template('err.tpl',msg="您上传的文件有错误，请重试！")

@route('/upload_ana', method='POST')
def upload():
    # category = request.forms.get('category')
    file = request.files.file
    if file:
        name, ext = os.path.splitext(file.filename)
        if ext not in ('.txt','.dat','.csv'):
            return template('err.tpl',msg="格式错误，请您上传文本文件，后缀为.txt,.dat或者csv")
        curpath = os.getcwd()

        # save_path = get_save_path_for_category(category)
        file.save(curpath+"/static/upload_data") # appends upload.filename automatically
        msg = name+ext
        return template('analysis.tpl',msg='')
    return template('err.tpl',msg="您上传的文件有错误，请重试！")

@route('/err/<msg>')
def error(msg):
    return template('err.tpl',err=msg)

@route('/vis_actor')
def index():
    return template('vis_actor')

@route('/vis_events')
def index():
    return template('vis_events')

@route('/coactor')
def index():
    return template('coactor.html')

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

@route('/lib/<path:path>')
def static(path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    return static_file(path, root=curdir + '/lib/')

@route('/crawl/<path:path>')
def static(path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    return static_file(path, root=curdir + '/crawl/')

# @error(404)
# def error404(error):
#     return template('404')

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 8081

run(server='auto', host='0.0.0.0', port=port, reloader=True, debug=True)
