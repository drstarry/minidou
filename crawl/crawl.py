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

    def get_url(self,id):
        return "http://www.douban.com/people/"+str(id)

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
        self.dr.get(url+'/contacts')
        article = self.dr.find_element_by_xpath('//div[@class="article"]')[0]
        try:
            aa = article.find_element_by_xpath('//dl[@class="obu"]/dd/a')
            for a in aa:
                href = a.find_element_by_xpath('@href')[0]
                uid = href.split('/')[-2]
                uid = a.find_element_by_xpath('text()')[0]
                urls.append(get_url(uid))
                f.write(str(curid)+' follow '+str(uid)+' '+name+'\n')
        except:
            pass

        #fans
        self.dr.get(url+'/rev_contacts')
        article = self.dr.find_element_by_xpath('//div[@class="article"]')[0]
        try:
            aa = article.find_element_by_xpath('//dl[@class="obu"]/dd/a')
            for a in aa:
                href = a.find_element_by_xpath('@href')[0]
                uid = href.split('/')[-2]
                uid = a.find_element_by_xpath('text()')[0]
                urls.append(get_url(uid))
                f.write(str(curid)+' follow '+str(uid)+' '+name+'\n')
        except:
            pass
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
