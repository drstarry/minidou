#encoding=utf-8
import requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time

class DoubanCrawler:
    def __init__(self,seeds,dr):
        #intialize
        self.linkQuence=linkQuence()
        self.dr=dr
        if isinstance(seeds,str):
            self.linkQuence.addUnvisitedUrl(seeds)
        if isinstance(seeds,list):
            for i in seeds:
                self.linkQuence.addUnvisitedUrl(i)
        print "Add the seeds url \"%s\" to the unvisited url list"%str(self.linkQuence.unVisited)

    def crawl_city(self,degree):
        """
        same city crawler
        """
        dg = degree
        while dg and self.linkQuence.unVisitedUrlsEnmpy() is False:
            #pop one link from unvisited
            visitUrl=self.linkQuence.unVisitedUrlDeQuence()
            print "Pop out one url \"%s\" from unvisited url list"%visitUrl
            if visitUrl is None or visitUrl=="":
                continue

            #get all links from this url
            links=self.get_friends(visitUrl)
            print "Get %d new links"%len(links)

            #remove this url from unvisited
            self.linkQuence.addVisitedUrl(visitUrl)
            print "Visited url count: "+str(self.linkQuence.getVisitedUrlCount())

            #put links into unvisited
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            print "%d unvisited links:"%len(self.linkQuence.getUnvisitedUrl())
            dg = dg -1

    def crawl_rel(self,degree):
        """
        relation crawler
        """
        dg = degree
        while dg and self.linkQuence.unVisitedUrlsEnmpy() is False:
            #pop one link from unvisited
            visitUrl=self.linkQuence.unVisitedUrlDeQuence()
            print "Pop out one url \"%s\" from unvisited url list"%visitUrl
            if visitUrl is None or visitUrl=="":
                continue

            #get all links from this url
            links=self.get_friends(visitUrl)
            print "Get %d new links"%len(links)

            #remove this url from unvisited
            self.linkQuence.addVisitedUrl(visitUrl)
            print "Visited url count: "+str(self.linkQuence.getVisitedUrlCount())

            #put links into unvisited
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            print "%d unvisited links:"%len(self.linkQuence.getUnvisitedUrl())
            dg = dg -1

    def get_friends(self,url):

        """
        get follow&fans urls and save, self.dr
        """

        urls = []
        print url
        curid = get_cur_id(url)
        f = open("friends.txt",'w')

        # follow
        page = urllib2.urlopen(url+"/follow").read()
        f = open('page.txt','w')
        f.write(page)
        dom = html.fromstring(page)

        # print dom.xpath('//script/text()')[1]

        pglist = dom.xpath('//div[@class="\"W_pages W_pages_comment S_line1\""]')[0]
        print pglist
        pgnum = len(pglist.xpath('a'))
        for i in range(1,pgnum):
            pgurl = url+"?page="+i+"#place"
            dom = html.fromstring(requests.get(pgurl).text)
            usrlist = dom.xpath('//ul[@class="cnfList"]/li')
            print 'usrlist',usrlist
            for li in usrlist:
                info = li.xpath('//div[@class="name"]')
                idcard = info.xpath('a[@class="W_f14 S_func1"]/@usercard')[0]
                uid = idcard.split('=')[1]
                urls.append(get_url(uid))
                name = info.xpath('a[@class="W_f14 S_func1"]/text()')[0]
                addr = ''
                try:
                    addrdic = info.xpath('span[@class="addr"]/text()')[0]
                    addr = '.'.join(addrdic.split(''))
                except:
                    pass
                f.write(str(curid)+' follow '+str(uid)+' '+name+' '+addr+'\n')

        #fans
        page = urllib2.urlopen(url+"/follow?relate=fans").read()
        dom = html.fromstring(page)
        pglist = dom.xpath("//div[@class='W_pages W_pages_comment S_line1']")[0]
        pgnum = len(pglist.xpath('a'))
        for i in range(1,pgnum):
            pgurl = url+"?relate=fans&page="+i+"#place"
            dom = html.fromstring(requests.get(pgurl).text)
            usrlist = dom.xpath('//ul[@class="cnfList"]/li')
            for li in usrlist:
                info = li.xpath('//div[@class="name"]')
                idcard = info.xpath('a[@class="W_f14 S_func1"]/@usercard')[0]
                uid = idcard.split('=')[1]
                urls.append(get_url(uid))
                name = info.xpath('a[@class="W_f14 S_func1"]/text()')[0]
                addr = ''
                try:
                    addrdic = info.xpath('span[@class="addr"]/text()')[0]
                    addr = '.'.join(addrdic.split(''))
                except:
                    pass
                f.write(str(curid)+' fanby '+str(uid)+' '+name+' '+addr+'\n')

        return urls


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

def login():
    dr=webdriver.PhantomJS('/usr/bin/phantomjs')
    dr.get("http://www.douban.com/")
    time.sleep(20)
    dr.find_element_by_id('form_email').send_keys('331993118@qq.com')
    dr.find_element_by_id('form_password').send_keys('dairui1991')
    dr.find_element_by_class_name('bn-submit').submit()
    return dr

def main(seed,degree):
    dr = login()
    seedurl = get_url(seed)
    crawl=DoubanCrawler(seedurl,dr)
    crawl.crawl_rel(degree)

if  __name__ == "__main__":
    main(1005052149890080,2)
