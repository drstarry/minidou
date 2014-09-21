#!env python2.7
#encoding: utf8

import sys
import os
import os.path
from bottle import route, run, template, static_file, request
import time
import json
from lib.crawl import DoubanCrawler
import pandas as pd
import urllib
import urllib2
import string
import jieba.analyse as ja


@route('/movie')
def movie():
    return template('movie')


@route('/event')
def event():
    return template('event')


@route('/crawl/<msg>', method='POST')
def crawl(msg):
    if msg == 'movie':
        pid = str(request.forms.get("id"))
        degree = str(request.forms.get("degree"))
        rtype = str(request.forms.get("rtype").split('.')[1])

        if pid and degree and rtype:
            print pid, degree, rtype
            seedurl = "http://movie.douban.com/subject/" + str(pid)
            # try:
            crawl = DoubanCrawler(seedurl)
            ca_json, movie, review = crawl.crawl_movie(degree, rtype)
            img = "static/img/mv_" + str(pid) + ".jpg"
            urllib.urlretrieve(movie['pic'], img)
            filename = 'static/vis_data/actor.json'
            f = open(filename, 'w')
            f.write(json.dumps(ca_json))
            f.close()

            f = open("static/vis_data/word_raw.txt", 'w')

            for r in review:
                for rf in r["bd_full"]:
                    f.write(rf.encode('utf-8'))

            word_count()
            return template('m_info.tpl', movie=movie, review=review, img='/' + img)
            # except:
            #     return template('err.tpl',err="您输入信息有误，请请重新输入准确的电影ID!")

        return template('err.tpl', err="您输入的信息不完整，请重新输入!")

    if msg == 'event':
        print request.forms
        etype = request.forms.get("etype").split('.')[0]
        type_name = request.forms.get("etype").split('.')[1]
        etime = request.forms.get("etime").split('.')[0]
        time_name = request.forms.get("etime").split('.')[1]
        print etype, etime
        if etype and etime:
            etime_l = ["today", "tomorrow", "weekend", "week"]
            etype_l = ["music", "drama", "salon", "party", "film", "exhibition", "sports", "commomwheel", "travel", "all"]
            seedurl = "http://beijing.douban.com/events/" + str(etime_l[int(etime) - 1]) + "-" + str(etype_l[int(etype) - 1])

            # try:
            c = DoubanCrawler(seedurl)
            events = c.crawl_event()

            data_to_js(events)
            return template('eventlist.tpl', events=events, etype=type_name, etime=time_name)
            # except:
            #     return template('err.tpl',err="您输入信息有误，请请重新输入!")

        return template('err.tpl', err="您输入的信息不完整，请重新输入!")
    return template('err.tpl', err="您输入的信息不完整，请重新输入!")


def data_to_js(events):
    f = open('static/vis_data/data.js', 'w')

    e_new = []
    for e in events:
        addr = ('').join(e['loc'].encode('utf-8').split())
        print addr
        try:
            geo = json.load(urllib2.urlopen("http://api.map.baidu.com/geocoder/v2/?address=" + addr + "&output=json&ak=FB4li2eKBB6HFRrws0N97qnW"))
            if geo["status"] == 0:
                lat = geo['result']['location']['lat']
                lon = geo['result']['location']['lng']
                e_new.append({'lat': lat, 'lon': lon, 'title': e['title'].encode('utf-8'), 'loc': e['loc'].encode('utf-8'), 'time': e['etime'].encode('utf-8')})
        except:
            pass

    df = pd.DataFrame(e_new)
    gr = df.groupby(['lat', 'lon'])

    f.write('var data =[\n')
    print gr.groups
    print type(gr.groups)
    for key, val in gr.groups.iteritems():
        f.write('[' + str(key[0]) + ',' + str(key[1]) + ',[\n')
        for idx, v in enumerate(val):
            if idx == 0:
                f.write('["' + string.replace(e_new[int(v)]['title'], '"', '^') + '","' + string.replace(e_new[int(v)]['loc'], '"', '^') + '","' + string.replace(e_new[int(v)]['time'], '"', '^') + '"]\n')
            else:
                f.write(',["' + string.replace(e_new[int(v)]['title'], '"', '^') + '","' + string.replace(e_new[int(v)]['loc'], '"', '^') + '","' + string.replace(e_new[int(v)]['time'], '"', '^') + '"]\n')
        f.write(']],\n')
    f.write('];\n')


@route('/map')
def map():
    return template('map.html')


@route('/eventlist')
def eventlist():
    return template('eventlist')


@route('/words')
def words():
    return template('words.html')


@route('/vis_review')
def vis_review():
    return template('vis_review.tpl', msg='')


def word_count():
    text = ''
    fr = open('static/vis_data/word_raw.txt', 'r')
    for line in fr.read():
        if line:
            text += line

    words = ja.extract_tags(text, 30)
    fr.close()

    fw = open('static/vis_data/words.csv', 'w')
    fw.write('text,size\n')
    for idx, w in enumerate(words):
        fw.write(w.encode('utf-8') + ',' + str((30 - idx) * (30 - idx)) + '\n')


@route('/upload_review', method='POST')
def upload():
    # category = request.forms.get('category')
    upload = request.files.get('file')
    print type(upload)
    if upload:
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.txt'):
            return template('err.tpl', err="格式错误，请您上传.txt文件")

        curpath = os.getcwd()
        print curpath

        try:
            os.system("rm " + curpath + "/static/upload_data/word_raw.txt")
        except:
            pass
        f = open(curpath + "/static/upload_data/word_raw.txt", 'w')

        f.write(upload.file.read())

        try:
            os.system("rm " + curpath + "/static/vis_data/word_raw.txt")
        except:
            pass

        os.system("cp " + curpath + "/static/upload_data/word_raw.txt " + curpath + "/static/vis_data/word_raw.txt")

        time.sleep(5)

        word_count()

        return template('vis_review.tpl', msg=name + ext)
    return template('err.tpl', err="您上传的文件有错误，请重试！")


@route('/err/<msg>')
def err(msg):
    return template('err.tpl', err=msg)


@route('/vis_actor')
def vis_actor():
    return template('vis_actor.tpl', msg='')


@route('/vis_events')
def vis_events():
    return template('vis_events.tpl', msg='')


@route('/coactor')
def coactor():
    return template('coactor.html')


@route('/')
def index():
    return template('index')


@route('/about')
def about():
    return template('about')


@route('/help')
def help():
    return template('help')


@route('/static/<path:path>')
def static(path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    return static_file(path, root=curdir + '/static/')


@route('/lib/<path:path>')
def lib(path):
    curdir = os.path.dirname(os.path.realpath(__file__))
    return static_file(path, root=curdir + '/lib/')


if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 8080

run(server='auto', host='0.0.0.0', port=port, reloader=True, debug=True)
