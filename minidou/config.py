#!/usr/bin/python
# coding: utf-8

import os

PORT = 8080

def get_project_root_dir():
    import minidou
    return os.path.abspath(os.path.dirname(os.path.dirname(minidou.__file__)))


#path config
ROOT_PATH = get_project_root_dir() + '/minidou'
TEMPLATE_PATH = ROOT_PATH + '/view'
STATIC_PATH = ROOT_PATH + '/static'

#crawler config
event_base_url = "http://beijing.douban.com/events/"
event_time = ["today", "tomorrow", "weekend", "week"]
event_type = ["music", "drama", "salon", "party", "film", "exhibition", "sports", "commonweal", "travel", "all"]
