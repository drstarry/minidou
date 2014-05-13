#encoding=utf-8
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
import urllib,urllib2
import re
import json

class DoubanCrawler:
    def __init__(self,seeds):
        #intialize
        self.linkQuence=linkQuence()
        self.current_deepth = 1
        if isinstance(seeds,str):
            self.linkQuence.addUnvisitedUrl(seeds)
        if isinstance(seeds,list):
            for i in seeds:
                self.linkQuence.addUnvisitedUrl(i)
        print "Add the seeds url \"%s\" to the unvisited url list"%str(self.linkQuence.unVisited)

    def get_url(self,id):
        return "http://www.douban.com/people/"+str(id)

    def crawl_movie(self,degree,rtype):
        movie = self.crawl_mv_info()
        coactor = self.crawl_actor(degree)
        review = self.crawl_review(rtype)
        return coactor,movie,review

    def crawl_mv_info(self):
        movie = {}

        visitUrl=self.linkQuence.unVisitedUrlDeQuence()
        print "Pop out one url \"%s\" from unvisited url list"%visitUrl

        page = urllib2.urlopen(visitUrl).read()
        dom = html.fromstring(page)
        actors = dom.xpath('//div[@class="subject clearfix"]/div[@id="info"]/span')[2].xpath('a')
        a_list = []

        for a in actors:
            href = a.xpath('@href')[0]
            pid = href.split('/')[-2]
            self.linkQuence.addUnvisitedUrl("http://movie.douban.com"+href)
            print 'add url "%s"to unvisited'%href
            name = a.xpath('text()')[0]
            a_list.append({'pid':pid,'name':name,'href':
                "http://movie.douban.com"+href})

        movie['actors'] = a_list
        content = dom.xpath('//div[@id="content"]')[0]
        movie['title'] = content.xpath('h1/span[@property="v:itemreviewed"]/text()')[0]
        movie['year'] = content.xpath('h1/span[@class="year"]/text()')[0]
        movie['director'] = dom.xpath('//div[@class="subject clearfix"]/div[@id="info"]/span')[0].xpath('a/text()')
        movie['bianju'] = dom.xpath('//div[@class="subject clearfix"]/div[@id="info"]/span')[1].xpath('a/text()')
        movie['mtype'] = dom.xpath('//span[@property="v:genre"]/text()')
        movie['summery'] = dom.xpath('//span[@property="v:summary"]/text()')
        movie['pic'] = dom.xpath('//div[@id="mainpic"]/a/img/@src')[0]
        movie['href'] = visitUrl

        self.linkQuence.addVisitedUrl(visitUrl)
        print "Visited url count: "+str(self.linkQuence.getVisitedUrlCount())
        # print movie
        return movie
    def crawl_review(self,rtype):
        pass

    def crawl_actor(self,degree):
        """
        movie actor crawler
        """
        dg = int(degree)
        coactor = []
        link_list = []
        # maxnum = 1000

        while self.current_deepth <= dg:
            while self.linkQuence.unVisitedUrlsEnmpy() is False:
                #pop one link from unvisited
                visitUrl=self.linkQuence.unVisitedUrlDeQuence()
                print "Pop out one url \"%s\" from unvisited url list"%visitUrl
                if visitUrl is None or visitUrl=="":
                    continue

                #get all links from this url
                links,ca_list=self.get_actor(visitUrl)
                print "Get %d new links"%len(links)

                for ca in ca_list:
                    coactor.append(ca)
                for l in links:
                    link_list.append(l)

                #remove this url from unvisited
                self.linkQuence.addVisitedUrl(visitUrl)
                print "Visited url count: "+str(self.linkQuence.getVisitedUrlCount())
                print "Visited deepth: "+str(self.current_deepth)
                print "%d unvisited links:"%len(self.linkQuence.getUnvisitedUrl())

            #put links into unvisited
            for link in link_list:
                self.linkQuence.addUnvisitedUrl(link)
            print "add %d unvisited links:"%len(self.linkQuence.getUnvisitedUrl())


            self.current_deepth += 1

        # coactorset =  list(set(coactor))
        # print len(coactor),coactor
        return coactor

    def get_actor(self,url):
        ca_list = []
        links = []
        curid = url.split('/')[-2]
        page = urllib2.urlopen(url).read()
        f = open('actors.txt','a')
        dom = html.fromstring(page)
        name = dom.xpath('//div[@id="content"]')[0].xpath('h1/text()')[0].split()[0]
        nurl = url+'partners'
        page = urllib2.urlopen(nurl).read()
        dom = html.fromstring(page)
        pg_class = dom.xpath('//div[@class="paginator"]/span')
        if len(pg_class)>0:
            pg = len(pg_class)-1
        else:
            pg = 2
        print 'pg',pg
        for p in range(1,pg):
            newurl = nurl+'?start='+str((p-1)*10)
            page = urllib2.urlopen(newurl).read()
            dom = html.fromstring(page)
            a_list = dom.xpath('//div[@class="article"]/div/div[@class="partners item"]')
            for a in a_list:
                _name = a.xpath('div[@class="info"]/h2/a/text()')[0].split()[0]
                _id = a.xpath('@id')[0]
                href = a.xpath('div[@class="info"]/h2/a/@href')[0]
                weight = len(a.xpath('div[@class="info"]/ul/li/a'))
                links.append(href)

                # print 'add url "%s"to unvisited'%href
                f.write(curid+"#"+name.encode('utf-8')+" "+_id+"#"+_name.encode('utf-8')+"\n")
                ca_list.append({'source':curid,'target':_id,'weight':weight})
        # print 'links',links
        return links,ca_list

    def crawl_event(self):
        """
        same city event crawler
        """
        events = []
        while self.linkQuence.unVisitedUrlsEnmpy() is False:
            #pop one link from unvisited
            visitUrl=self.linkQuence.unVisitedUrlDeQuence()
            print "Pop out one url \"%s\" from unvisited url list"%visitUrl
            if visitUrl is None or visitUrl=="":
                continue

            #get all links from this url
            links,events=self.get_events(visitUrl)
            print "Get %d new links"%len(links)

            #remove this url from unvisited
            self.linkQuence.addVisitedUrl(visitUrl)
            print "Visited url count: "+str(self.linkQuence.getVisitedUrlCount())

            #put links into unvisited
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            print "%d unvisited links:"%len(self.linkQuence.getUnvisitedUrl())

        return events

    def get_events(self,url):
        e_list = []
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(url,headers=headers)
        page = urllib2.urlopen(req).read()
        f = open('events.txt','w')

        dom = html.fromstring(page)
        try:
            page = dom.xpath('//div[@id="db-events-list"]/div[@class="paginator"]/span[@class="thispage"]/@data-total-page')[0]
            print 'page',page
        except:
            page = 1

        for i in range(1,int(page)):

            url_new = url+"?start="+str((i-1)*10)
            req = urllib2.Request(url_new,headers=headers)
            page = urllib2.urlopen(req).read()
            dom = html.fromstring(page)
            events = dom.xpath('//ul[@class="events-list events-list-pic100 events-list-psmall"]/li')
            for e in events:
                info = e.xpath('div[@class="info"]')[0]
                title = info.xpath('div[@class="title"]/a/span/text()')[0]
                href =  info.xpath('div[@class="title"]/a/@href')[0]
                pic = e.xpath('div[@class="pic"]/a/img/@data-lazy')[0]
                try:
                    tags = info.xpath('p[@class="event-cate-tag hidden-xs"]/a/text()')
                except:
                    tags = []
                ul = info.xpath('ul[@class="event-meta"]')[0]
                etime = ul.xpath('li[@class="event-time"]/text()')[1].strip()
                loc = ul.xpath('li/meta[@itemprop="location"]/@content')[0]
                latitude = ul.xpath('//meta[@itemprop="latitude"]/@content')[0]
                longtitude = ul.xpath('//meta[@itemprop="longitude"]/@content')[0]
                fee = ul.xpath('li[@class="fee"]/strong/text()')
                counts = info.xpath('p[@class="counts"]/span/text()')
                # print counts
                re_go_count = re.match(r'^(\d*).*$',counts[0])
                go_count = re_go_count.group(1)
                re_like_count = re.match(r'^(\d*).*$',counts[1])
                like_count = re_like_count.group(1)
                e_list.append({'title':title,'href':href,'pic':pic,'tags':tags,'etime':etime,'loc':loc,'latitude':latitude,'longtitude':longtitude,'fee':fee,'go_count':go_count,'like_count':like_count})

        # print e_list
        # print 'num',len(e_list)
        # json.dump(e_list,f)

        return [],e_list

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

# def movie_crawl(seedid,degree,rtype):
#     seedurl = "http://movie.douban.com/subject/"+str(seedid)
#     crawl=DoubanCrawler(seedurl)
#     crawl.crawl_movie(degree)

def event_crawl(etype,etime):
    etime_l = ["today","tomorrow","weekend","week"]
    etype_l = ["music","drama","salon","party","film","exhibition","sports","commomwheel","travel","all"]
    seedurl = "http://beijing.douban.com/events/"+str(etime_l[int(etime)-1])+"-"+str(etype_l[int(etype)-1])
    crawl=DoubanCrawler(seedurl)
    events = crawl.crawl_event()
    return events

# if  __name__ == "__main__":
#     arg = sys.argv
#     print arg
#     if arg[1] == '1':
#         print 'movie crawl'
#         mid = arg[2]
#         degree = arg[3]
#         rtype = arg[4]
#         movie_crawl(mid,degree,rtype)

#     if arg[1] == '2':
#         print 'event crawl'
#         etype = arg[2]
#         etime = arg[3]
#         event_crawl(etype,etime)
