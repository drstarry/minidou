#!/usr/bin/env python2
# encoding: utf8

import json
import os
import time
import urllib

import bottle
from bottle import route, run, template, request, static_file
from minidou.lib.crawl import DoubanCrawler
from minidou.lib.util import word_count
from minidou.lib.util import data_to_js
from minidou.config import ROOT_PATH, STATIC_PATH, TEMPLATE_PATH, event_base_url, event_time, event_type

bottle.TEMPLATE_PATH.append(TEMPLATE_PATH)


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
            seedurl = "http://movie.douban.com/subject/" + str(pid)
            crawl = DoubanCrawler(seedurl)
            ca_json, movie, review = crawl.crawl_movie(degree, rtype)
            img = "/img/mv_" + str(pid) + ".jpg"
            urllib.urlretrieve(movie['pic'], STATIC_PATH + img)
            filename = STATIC_PATH + '/vis_data/actor.json'

            with open(filename, 'w') as f:
                f.write(json.dumps(ca_json))

            with open(STATIC_PATH + "/vis_data/word_raw.txt", 'w') as f:
                for r in review:
                    for rf in r["bd_full"]:
                        f.write(rf.encode('utf-8'))

            word_count()

            return template('m_info.tpl', movie=movie, review=review, img='/static' + img)

    if msg == 'event':
        etype = request.forms.get("etype").split('.')[0]
        type_name = request.forms.get("etype").split('.')[1]
        etime = request.forms.get("etime").split('.')[0]
        time_name = request.forms.get("etime").split('.')[1]

        if etype and etime:
            seedurl = event_base_url + str(event_time[int(etime) - 1]) + "-" + str(
                event_type[int(etype) - 1])

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
    upload = request.files.get('file')
    if upload:
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.txt'):
            return template('err.tpl', err="error! .txt only!")

        try:
            os.system("rm " + STATIC_PATH + "/upload_data/word_raw.txt")
        except:
            pass

        with open(STATIC_PATH + "/upload_data/word_raw.txt", 'w') as f:
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
    return template('index')


@route('/about')
def about():
    return template('about')


@route('/help')
def help():
    return template('help')


@route('/static/<path:path>')
def static(path):
    return static_file(path, root=STATIC_PATH)


def run_server(port, debug=True):
    run(server='auto', host='0.0.0.0', port=port, reloader=debug, debug=debug)

