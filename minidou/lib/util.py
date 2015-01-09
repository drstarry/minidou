#!env python
#encoding: utf8

import json
import os
import string
import urllib2

import jieba.analyse as ja
import pandas as pd
import xmltodict

from minidou.config import STATIC_PATH

def word_count():

    text = ''
    with open(STATIC_PATH + '/vis_data/word_raw.txt', 'r') as fr:
        for line in fr.read():
            if line:
                text += line

    words = ja.extract_tags(text, 30)

    with open(STATIC_PATH + '/vis_data/words.csv', 'w') as fw:
        fw.write('text,size\n')
        for idx, w in enumerate(words):
            fw.write(w.encode('utf-8') + ',' + str((30 - idx) * (30 - idx)) + '\n')


def data_to_js(events):
    f = open(STATIC_PATH + '/vis_data/data.js', 'w')

    e_new = []
    for e in events:
        addr = ('').join(e['loc'].encode('utf-8').split())
        #print addr
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
#
    for key, val in gr.groups.iteritems():
        f.write('[' + str(key[0]) + ',' + str(key[1]) + ',[\n')
        for idx, v in enumerate(val):
            if idx == 0:
                f.write('["' + string.replace(e_new[int(v)]['title'], '"', '^') + '","' + string.replace(e_new[int(v)]['loc'], '"', '^') + '","' + string.replace(e_new[int(v)]['time'], '"', '^') + '"]\n')
            else:
                f.write(',["' + string.replace(e_new[int(v)]['title'], '"', '^') + '","' + string.replace(e_new[int(v)]['loc'], '"', '^') + '","' + string.replace(e_new[int(v)]['time'], '"', '^') + '"]\n')
        f.write(']],\n')
    f.write('];\n')

    f.close()


def get_useragents_list():
    pass

