#!env python2.7
#encoding: utf8
import sys
import os
import os.path
import jieba
from bottle import route, run, template, view, static_file, request, urlencode, redirect,error
import time
import json
from lib.crawl import DoubanCrawler
import json
import pandas as pd
import urllib2,urllib
import string


@route('/movie')
def index():
    return template('movie')

@route('/event')
def index():
    return template('event')

@route('/crawl/<msg>', method='POST')
def crawl(msg):
    if msg == 'movie':
        pid = str(request.forms.get("id"))
        degree = str(request.forms.get("degree"))
        rtype = str(request.forms.get("rtype").split('.')[1])

        if pid and degree and rtype:
            print pid,degree,rtype
            seedurl = "http://movie.douban.com/subject/"+str(pid)
            # try:
            crawl=DoubanCrawler(seedurl)
            ca_json,movie,review = crawl.crawl_movie(degree,rtype)
            img = "static/img/mv_"+str(pid)+".jpg"
            urllib.urlretrieve(movie['pic'], img)
            filename = 'static/vis_data/actor.json'
            f = open(filename,'w')
            f.write(json.dumps(ca_json))
            f.close()
            print 'actor',ca_json
            print 'movie',movie
            return template('m_info.tpl',movie=movie,review=review,img='/'+img)
            # except:
            #     return template('err.tpl',err="您输入信息有误，请请重新输入准确的电影ID!")

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

            # try:
            c=DoubanCrawler(seedurl)
            events = c.crawl_event()

            data_to_js(events)
            return template('eventlist.tpl', events=events,etype=type_name,etime=time_name)
            # except:
            #     return template('err.tpl',err="您输入信息有误，请请重新输入!")

        return template('err.tpl',err="您输入的信息不完整，请重新输入!")
    return template('err.tpl',err="您输入的信息不完整，请重新输入!")

def data_to_js(events):
    f = open('static/vis_data/data.js','w')

    e_new = []
    for e in events:
        addr = ('').join(e['loc'].encode('utf-8').split())
        print addr
        try:
            geo = json.load(urllib2.urlopen("http://api.map.baidu.com/geocoder/v2/?address="+addr+"&output=json&ak=FB4li2eKBB6HFRrws0N97qnW"))
            if geo["status"] == 0:
                lat = geo['result']['location']['lat']
                lon = geo['result']['location']['lng']
                print lat,lon,addr
                e_new.append({'lat':lat,'lon':lon,'title':e['title'].encode('utf-8'),'loc':e['loc'].encode('utf-8'),'time':e['etime'].encode('utf-8')})
        except:
            pass

    df = pd.DataFrame(e_new)
    gr =  df.groupby(['lat','lon'])

    f.write('var data =[\n')
    print gr.groups
    print type(gr.groups)
    for key,val in gr.groups.iteritems():
        print 'key',key
        print 'val',val
        f.write('['+str(key[0])+','+str(key[1])+',[\n')
        for idx,v in enumerate(val):
            if idx==0:
                f.write('["'+string.replace(e_new[int(v)]['title'],'"','^')+'","'+string.replace(e_new[int(v)]['loc'],'"','^')+'","'+string.replace(e_new[int(v)]['time'],'"','^')+'"]\n')
            else:
               f.write(',["'+string.replace(e_new[int(v)]['title'],'"','^')+'","'+string.replace(e_new[int(v)]['loc'],'"','^')+'","'+string.replace(e_new[int(v)]['time'],'"','^')+'"]\n')
        f.write(']],\n')
    f.write('];\n')


@route('/map')
def map():
    return template('map.html')

@route('/eventlist')
def eve_list():
    return template('eventlist')

@route('/words')
def eve_list():
    return template('words.html')

@route('/vis_review')
def eve_list():
    return template('vis_review')


@route('/upload_vis', method='POST')
def upload():
    # category = request.forms.get('category')
    file = request.files.file
    if file:
        name, ext = os.path.splitext(file.filename)
        if ext not in ('.js'):
            return template('err.tpl',err="格式错误，请您上传文本文件，后缀为.txt,.dat或者csv")
        curpath = os.getcwd()

        # save_path = get_save_path_for_category(category)
        file.save(curpath+"/static/upload_data") # appends upload.filename automatically
        msg = name+ext
        return template('visual.tpl',msg='')
    return template('err.tpl',msg="您上传的文件有错误，请重试！")

@route('/upload_ana', method='POST')
def upload():
    # category = request.forms.get('category')
    upload = request.files.get('file')
    print type(upload)
    if upload:
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.json'):
            return template('err.tpl',err="格式错误，请您上传.json文件")

        curpath = os.getcwd()
        print curpath
        # save_path = get_save_path_for_category(category)
        upload.save(curpath+"/static/upload_data") # appends upload.filename automatically
        msg = name+ext
        return template('analysis.tpl',err='')
    return template('err.tpl',err="您上传的文件有错误，请重试！")

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


if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 8081

run(server='auto', host='0.0.0.0', port=port, reloader=True, debug=True)
