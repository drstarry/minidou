#!env python2.7
#encoding: utf8

import bottle
from bottle import route, run, template, static_file, request
import json
import os
import os.path
import time
import urllib

from minidou.lib.crawl import DoubanCrawler
from minidou.lib.util import word_count
from minidou.lib.util import data_to_js
from minidou.config import PORT, ROOT_PATH, TEMPLATE_PATH, STATIC_PATH

bottle.TEMPLATE_PATH.insert(0, '/Users/Starry/Work/proj/play/minidou/minidou/view')
curpath = os.getcwd()


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
            crawl = DoubanCrawler(seedurl)
            ca_json, movie, review = crawl.crawl_movie(degree, rtype)
            img = STATIC_PATH + "/img/mv_" + str(pid) + ".jpg"
            print img
            urllib.urlretrieve(movie['pic'], img)
            filename = STATIC_PATH + '/vis_data/actor.json'
            with open(filename, 'w') as f:
                f.write(json.dumps(ca_json))

            with open(STATIC_PATH + "/vis_data/word_raw.txt", 'w') as f:
                for r in review:
                    for rf in r["bd_full"]:
                        f.write(rf.encode('utf-8'))

            word_count()

            return template('m_info.tpl', movie=movie, review=review, img='/' + img)

    if msg == 'event':
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

    return template('err.tpl', err="incomplete info! try again!")


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


@route('/upload_review', method='POST')
def upload():
    # category = request.forms.get('category')
    upload = request.files.get('file')
    print type(upload)
    if upload:
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.txt'):
            return template('err.tpl', err="error! .txt only!")

        try:
            os.system("rm " + STATIC_PATH + "/upload_data/word_raw.txt")
        except:
            pass

        with open(curpath + STATIC_PATH + "/upload_data/word_raw.txt", 'w') as f:
            f.write(upload.file.read())

        try:
            os.system("rm " + STATIC_PATH + "/vis_data/word_raw.txt")
        except:
            pass

        os.system("cp " + STATIC_PATH + "/upload_data/word_raw.txt " + STATIC_PATH + "/vis_data/word_raw.txt")

        time.sleep(5)

        word_count()

        return template('vis_review.tpl', msg=name + ext)
    return template('err.tpl', err="err when uploading, try again!")


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
    curdir = os.getcwd()
    print curdir
    return template('index')


@route('/about')
def about():
    return template('about')


@route('/help')
def help():
    return template('help')

"""
@route('/static/<path:path>')
def static(path):
    curdir = os.getcwd()
    print curdir
    return static_file(path, root=curdir + '/minidou/static/')


@route('/lib/<path:path>')
def lib(path):
    curdir = os.getcwd()
    print curdir
    return static_file(path, root=curdir + '/minidou/lib/')


@route('/view/<path:path>')
def view(path):
    curdir = os.getcwd()
    return static_file(path, root=curdir + '/minidou/view/')
"""


def run_server(port):
    run(server='auto', host='0.0.0.0', port=PORT, reloader=True, debug=True)
