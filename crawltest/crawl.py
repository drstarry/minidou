#encoding=utf-8
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
import urllib,urllib2
import re

class DoubanCrawler:
    def __init__(self,seeds):
        #intialize
        self.linkQuence=linkQuence()
        if isinstance(seeds,str):
            self.linkQuence.addUnvisitedUrl(seeds)
        if isinstance(seeds,list):
            for i in seeds:
                self.linkQuence.addUnvisitedUrl(i)
        print "Add the seeds url \"%s\" to the unvisited url list"%str(self.linkQuence.unVisited)

    # def login(self):
    #     """
    #     log in by phantomjs
    #     """
    #     dr=webdriver.PhantomJS('/usr/bin/phantomjs')
    #     dr.get("http://www.douban.com/")
    #     time.sleep(20)
    #     dr.find_element_by_id('form_email').send_keys('331993118@qq.com')
    #     dr.find_element_by_id('form_password').send_keys('dairui1991')
    #     dr.find_element_by_class_name('bn-submit').submit()
    #     return dr

    def get_url(self,id):
        return "http://www.douban.com/people/"+str(id)

    def crawl_event(self):
        """
        same city event crawler
        """
        # dg = degree
        while self.linkQuence.unVisitedUrlsEnmpy() is False:
            #pop one link from unvisited
            visitUrl=self.linkQuence.unVisitedUrlDeQuence()
            print "Pop out one url \"%s\" from unvisited url list"%visitUrl
            if visitUrl is None or visitUrl=="":
                continue

            #get all links from this url
            links=self.get_events(visitUrl)
            print "Get %d new links"%len(links)

            #remove this url from unvisited
            self.linkQuence.addVisitedUrl(visitUrl)
            print "Visited url count: "+str(self.linkQuence.getVisitedUrlCount())

            #put links into unvisited
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            print "%d unvisited links:"%len(self.linkQuence.getUnvisitedUrl())
            # dg = dg -1

    def get_events(self,url):
        e_list = []
        page = urllib2.urlopen(url).read()
        f = open('events.txt','w')

        dom = html.fromstring(page)
        try:
            page = dom.xpath('//div[@id="db-events-list"]/div[@class="paginator"]/span[@class="thispage"]/@data-total-page')[0]
            print 'page',page
        except:
            page = 1

        for i in range(1,int(page)):
            url_new = url+"?start="+str((i-1)*10)
            page = urllib2.urlopen(url_new).read()
            dom = html.fromstring(page)
            events = dom.xpath('//ul[@class="events-list events-list-pic100 events-list-psmall"]/li')
            for e in events:
                info = e.xpath('div[@class="info"]')[0]
                title = info.xpath('div[@class="title"]/a/span/text()')[0]
                href =  info.xpath('div[@class="title"]/a/@href')[0]
                try:
                    tags = info.xpath('p[@class="event-cate-tag hidden-xs"/a/text()]')
                except:
                    tags = []
                    pass
                ul = info.xpath('ul[@class="event-meta"]')[0]
                etime = ul.xpath('li[@class="event-time"]/text()')
                loc = ul.xpath('li/meta[@itemprop="location"]/@content')[0]
                latitude = ul.xpath('//meta[@itemprop="latitude"]/@content')[0]
                longtitude = ul.xpath('//meta[@itemprop="longitude"]/@content')[0]
                fee = ul.xpath('li[@class="fee"]/strong/text()')
                counts = info.xpath('p[@class="counts"]/span/text()')
                print counts
                re_go_count = re.match(r'^(\d*).*$',counts[0])
                go_count = re_go_count.group(1)
                re_like_count = re.match(r'^(\d*).*$',counts[1])
                like_count = re_like_count.group(1)
                e_list.append({'title':title,'herf':href,'tags':tags,'etime':etime,'loc':loc,'latitude':latitude,'longtitude':longtitude,'fee':fee,'go_count':go_count,'like_count':like_count})

        print e_list
        print 'num',len(e_list)
        f.dump(e_list)

        return []

    # def crawl_rel(self,degree):
    #     """
    #     relation crawler
    #     """
    #     dg = degree
    #     while dg and self.linkQuence.unVisitedUrlsEnmpy() is False:
    #         #pop one link from unvisited
    #         visitUrl=self.linkQuence.unVisitedUrlDeQuence()
    #         print "Pop out one url \"%s\" from unvisited url list"%visitUrl
    #         if visitUrl is None or visitUrl=="":
    #             continue

    #         #get all links from this url
    #         links=self.get_friends(visitUrl)
    #         print "Get %d new links"%len(links)

    #         #remove this url from unvisited
    #         self.linkQuence.addVisitedUrl(visitUrl)
    #         print "Visited url count: "+str(self.linkQuence.getVisitedUrlCount())

    #         #put links into unvisited
    #         for link in links:
    #             self.linkQuence.addUnvisitedUrl(link)
    #         print "%d unvisited links:"%len(self.linkQuence.getUnvisitedUrl())
    #         dg = dg -1

    # def get_friends(self,url):

    #     """
    #     get follow&fans urls and save, self.dr
    #     """

    #     urls = []
    #     print url
    #     curid =url.split('/')[-2]
    #     f = open("friends.txt",'w')

    #     dr=webdriver.PhantomJS('/usr/bin/phantomjs')


    #     # follow
    #     dr.get(url+'/contacts')
    #     time.sleep(5)
    #     dr.find_element_by_id('email').send_keys('331993118@qq.com')
    #     dr.find_element_by_id('password').send_keys('dairui1991')
    #     dr.find_element_by_class_name('btn-submit').submit()
    #     time.sleep(10)
    #     source = dr.page_source
    #     print source
    #     dom = html.fromstring(source)


    #     try:
    #         aa = dom.xpath('//div[@class="article"]/dl')
    #         print "follow list:",aa
    #         for a in aa:
    #             print 'a,',a
    #             href = a.xpath('dd/a/@href')
    #             print 'url:',href
    #             uid = href.split('/')[-2]
    #             name = a.xpath('dd/a/text()')[0]
    #             print 'name:',name
    #             urls.append(get_url(uid))
    #             f.write(str(curid)+' follow '+str(uid)+' '+name+'\n')
    #     except:
    #         pass

    #     #fans
    #     dr.get(url+'/rev_contacts')
    #     time.sleep(5)
    #     dr.find_element_by_id('email').send_keys('331993118@qq.com')
    #     dr.find_element_by_id('password').send_keys('dairui1991')
    #     dr.find_element_by_class_name('btn-submit').submit()
    #     source = dr.page_source
    #     dom = html.fromstring(source)

    #     article = dom.xpath('//div[@class="article"]')
    #     print 'article:',article
    #     try:
    #         try:
    #             page = dom.xpath('//div[@class="paginator"]')
    #             print 'page:',page
    #             count = int(re.match(r'^.*?(\d*).*$',page.xpath('span[@class="count"]/text()')[0]).group(1))
    #             print 'page count:',count
    #             for i in range(1,count):
    #                 start = (i-1)*70
    #                 dr.get(url+'rev_contacts?start='+start)
    #                 time.sleep(5)
    #                 dr.find_element_by_id('email').send_keys('331993118@qq.com')
    #                 dr.find_element_by_id('password').send_keys('dairui1991')
    #                 dr.find_element_by_class_name('btn-submit').submit()
    #                 time.sleep(5)
    #                 source = dr.page_source
    #                 dom = html.fromstring(source)
    #                 aa = dom.xpath('//div[@class="article"]/dl[@class="obu"]/dd/a')
    #                 print
    #                 for a in aa:
    #                     href = a.xpath('@href')
    #                     print 'url:',href
    #                     uid = href.split('/')[-2]
    #                     name = a.xpath('text()')[0]
    #                     print 'name:',name
    #                     urls.append(get_url(uid))
    #                     f.write(str(curid)+' followedby '+str(uid)+' '+name+'\n')
    #         except:
    #             aa = dom.xpath('//div[@class="article"]/dl[@class="obu"]/dd/a')
    #             print 'aa',aa
    #             for a in aa:
    #                 href = a.xpath('@href')[0]
    #                 uid = href.split('/')[-2]
    #                 name = a.xpath('text()')[0]
    #                 urls.append(get_url(uid))
    #                 f.write(str(curid)+' followedby '+str(uid)+' '+name+'\n')
    #     except:
    #         pass

    #     return list(set(urls))


class linkQuence:
    def __init__(self):
        self.visted=[]
        self.unVisited=[]


    def getVisitedUrl(self):
        """
        get visited urls
        """
        return self.visted


    def getUnvisitedUrl(self):
        """
        get unvisited urls
        """
        return self.unVisited


    def addVisitedUrl(self,url):
        """
        get follow urls and save
        """
        self.visted.append(url)


    def removeVisitedUrl(self,url):
        """
        remove visited urls
        """
        self.visted.remove(url)

    def unVisitedUrlDeQuence(self):
        """
        pop unvisited urls
        """
        try:
            return self.unVisited.pop()
        except:
            return None

    def addUnvisitedUrl(self,url):
        """
        deduplicate
        """
        if url!="" and url not in self.visted and url not in self.unVisited:
            self.unVisited.insert(0,url)

    def getVisitedUrlCount(self):
        """
        get num of visited url
        """
        return len(self.visted)

    def getUnvistedUrlCount(self):
        """
        get num of unvisited url
        """
        return len(self.unVisited)

    def unVisitedUrlsEnmpy(self):
        """
        unvisited is null
        """
        return len(self.unVisited)==0

def get_cur_id(url):
    """
    get current uid from its url
    """
    uid = url.split('/')[-1]
    return uid

def get_url(seed):
    """
    get url by a userid
    """
    url = "http://www.douban.com/people/"+str(seed)
    return url

def movie_crawl(seedid,degree,rtype):
    seedurl = "http://movie.douban.com/subject/"+str(seedid)
    crawl=DoubanCrawler(seedurl)
    crawl.crawl_actor(degree)
    crawl.crawl_review(rtype)

def event_crawl(etype,etime):
    etime_l = ["today","tomorrow","weekend","week"]
    etype_l = ["music","drama","salon","party","film","exhibition","sports","commomwheel","travel","all"]
    seedurl = "http://beijing.douban.com/events/"+str(etime_l[int(etime)-1])+"-"+str(etype_l[int(etype)-1])
    crawl=DoubanCrawler(seedurl)
    crawl.crawl_event()

if  __name__ == "__main__":
    arg = sys.argv
    print arg
    if arg[1] == '1':
        print 'movie crawl'
        mid = arg[2]
        degree = arg[3]
        rtype = arg[4]

    if arg[1] == '2':
        print 'event crawl'
        etype = arg[2]
        etime = arg[3]
        event_crawl(etype,etime)
