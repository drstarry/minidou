#!env python2.7
#encoding = utf-8

from lxml import html
import urllib2
import re
import os
import sys
import logging

from minidou.config import ROOT_PATH


class DoubanCrawler:

    def __init__(self, seeds):
        #intialize
        self.linkQuence = linkQuence()
        self.current_deepth = 1
        self.actorid = []
        self.actor = []
        self.group = []
        self.a_list = []
        if isinstance(seeds, str):
            self.linkQuence.addUnvisitedUrl(seeds)
        if isinstance(seeds, list):
            for i in seeds:
                self.linkQuence.addUnvisitedUrl(i)
        logging.info("Add the seeds url \" %s \" to the unvisited url list" % str(self.linkQuence.unVisited))

    def get_url(self, id):
        return "http://www.douban.com/celebrity/" + str(id)

    def crawl_movie(self, degree, rtype):
        movie, review = self.crawl_mv_info(rtype)
        coactor = self.crawl_actor(degree)
        ca_json = {"nodes": self.a_list, "links": coactor}
        return ca_json, movie, review

    def crawl_mv_info(self, rtype):
        movie = {}
        visitUrl = self.linkQuence.unVisitedUrlDeQuence()
        logging.info("Pop out one url \" %s \" from unvisited url list" % visitUrl)

        review = self.crawl_review(visitUrl, rtype)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(visitUrl, headers=headers)
        page = urllib2.urlopen(req).read()
        dom = html.fromstring(page)
        actors = dom.xpath('//div[@id="info"]/span[@class="actor"]/span[@class="attrs"]//a')
	#print 'actors:', actors
        a_list = []

        for a in actors:
	    href = a.xpath('@href')[0]
            pid = href.split('/')[-2]
            self.linkQuence.addUnvisitedUrl("http://movie.douban.com" + href)
            logging.info('add url " %s "to unvisited' % href)
            name = a.xpath('text()')[0]
            a_list.append({'pid': pid, 'name': name, 'href': "http://movie.douban.com" + href})

        movie['actors'] = a_list
        content = dom.xpath('//div[@id="content"]')[0]
        movie['title'] = content.xpath('h1/span[@property="v:itemreviewed"]/text()')[0]
        movie['year'] = content.xpath('h1/span[@class="year"]/text()')[0]
	info = content.xpath('//div[@id="info"]/span')

	movie['director'] = info[0].xpath('span[@class="attrs"]/a/text()')
	movie['bianju'] = info[1].xpath('span[@class="attrs"]/a/text()')

	movie['mtype'] = dom.xpath('//span[@property="v:genre"]/text()')
        movie['summery'] = dom.xpath('//span[@property="v:summary"]/text()')[0].strip()
        movie['pic'] = dom.xpath('//div[@id="mainpic"]/a/img/@src')[0]
        movie['href'] = visitUrl

        self.linkQuence.addVisitedUrl(visitUrl)
        logging.info("Visited url count: " + str(self.linkQuence.getVisitedUrlCount()))
        #print movie
        return movie, review

    def crawl_review(self, url, rtype):
        """
        get review of certain count
        """
        review = []
        url = url + "/reviews"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(url, headers=headers)
        page = urllib2.urlopen(req).read()
        dom = html.fromstring(page)
        allreviews = dom.xpath('//div[@class="review"]')
        sum = int(rtype)
        reviews = allreviews[:sum]
        for r in reviews:
            href = r.xpath('div[@class="review-hd"]/h3/a[2]/@href')[0]
            #print href
            title = r.xpath('div[@class="review-hd"]/h3/a[2]/text()')[0]
            #print title
            bd_short = r.xpath('div[@class="review-bd"]/div[@class="review-short"]/span/text()')[0]
            headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib2.Request(href, headers=headers)
            pagen = urllib2.urlopen(req).read()
            domn = html.fromstring(pagen)
            bd_full = domn.xpath('//div[@id="link-report"]/div/text()')
            review.append({'href': href, 'title': title, 'bd_short': bd_short, 'bd_full': bd_full})

        #print review
        return review

    def crawl_actor(self, degree):
        """
        movie actor crawler
        """
        dg = int(degree)
        # a_list = []
        link_list = []
        coactor = []
        # maxnum = 1000

        while self.current_deepth <= dg:
            while self.linkQuence.unVisitedUrlsEnmpy() is False:
                #pop one link from unvisited
                visitUrl = self.linkQuence.unVisitedUrlDeQuence()
                logging.info("Pop out one url \" %s \" from unvisited url list" % visitUrl)
                if visitUrl is None or visitUrl == "":
                    continue

                #get all links from this url
                links, ca_list = self.get_actor(visitUrl)
                logging.info("Get %d new links" % len(links))

                for ca in ca_list:
                    coactor.append(ca)
                for l in links:
                    link_list.append(l)

                #remove this url from unvisited
                self.linkQuence.addVisitedUrl(visitUrl)
                logging.info("Visited url count: " + str(self.linkQuence.getVisitedUrlCount()))
                logging.info("Visited deepth: " + str(self.current_deepth))
                logging.info("%d unvisited links:" % len(self.linkQuence.getUnvisitedUrl()))

            #put links into unvisited
            for link in link_list:
                self.linkQuence.addUnvisitedUrl(link)
            logging.info("add %d unvisited links:" % len(self.linkQuence.getUnvisitedUrl()))

            self.current_deepth += 1

        # coactorset =  list(set(coactor))
        #print len(coactor), coactor
        return coactor

    def get_actor(self, url):
        ca_list = []
        links = []
        curid = url.split('/')[-2]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(url, headers=headers)
        page = urllib2.urlopen(req).read()
        f = open(ROOT_PATH + '/minidou/lib/data/actors.txt', 'a')
        dom = html.fromstring(page)
        try:
            name = dom.xpath('//div[@id="content"]')[0].xpath('h1/text()')[0].split()[0]

            if curid not in self.actorid:
                self.actorid.append(curid)
                self.actor.append(name)
                ngroup = self.actorid.index(curid)
                self.group.append(ngroup)
                self.a_list.append({"name": name, "group": ngroup})

            nurl = url + 'partners'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
            req = urllib2.Request(nurl, headers=headers)
            page = urllib2.urlopen(req).read()
            dom = html.fromstring(page)
            pg_class = dom.xpath('//div[@class="paginator"]/span')
            if len(pg_class) > 0:
                pg = len(pg_class) - 1
            else:
                pg = 2
            #print 'pg', pg
            for p in range(1, pg):
                newurl = nurl + '?start=' + str((p - 1) * 10)
                headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
                req = urllib2.Request(newurl, headers=headers)
                page = urllib2.urlopen(req).read()
                dom = html.fromstring(page)
                a_list = dom.xpath('//div[@class="article"]/div/div[@class="partners item"]')
                for a in a_list:
                    _name = a.xpath('div[@class="info"]/h2/a/text()')[0].split()[0]
                    _id = a.xpath('@id')[0]
                    href = a.xpath('div[@class="info"]/h2/a/@href')[0]
                    weight = len(a.xpath('div[@class="info"]/ul/li/a'))
                    links.append(href)

                    if _id not in self.actorid:
                        # print 'append into actor list:', _id
                        self.actorid.append(_id)
                        self.actor.append(_name)
                        # self.group.append(ngroup)
                        if len(self.group) == 0:
                            self.group.append(1)
                        self.a_list.append({"name": _name, "group": self.group[-1]})

                    # print 'add url "%s"to unvisited'%href
                    f.write(curid + "#" + name.encode('utf-8') + " " + _id + "#" + _name.encode('utf-8') + "\n")
                    ca_list.append({'source': self.actorid.index(curid), 'target': self.actorid.index(_id), 'weight': weight})
        except:
            pass
        # print 'links', links
        return links, ca_list

    def crawl_event(self):
        """
        same city event crawler
        """
        events = []
        while self.linkQuence.unVisitedUrlsEnmpy() is False:
            #pop one link from unvisited
            visitUrl = self.linkQuence.unVisitedUrlDeQuence()
            logging.info("Pop out one url \" %s \" from unvisited url list" % visitUrl)
            if visitUrl is None or visitUrl == "":
                continue

            #get all links from this url
            links, events = self.get_events(visitUrl)
            logging.info("Get %d new links" % len(links))

            #remove this url from unvisited
            self.linkQuence.addVisitedUrl(visitUrl)
            logging.info("Visited url count: " + str(self.linkQuence.getVisitedUrlCount()))

            #put links into unvisited
            for link in links:
                self.linkQuence.addUnvisitedUrl(link)
            logging.info("%d unvisited links:" % len(self.linkQuence.getUnvisitedUrl()))

        return events

    def get_events(self, url):
        e_list = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(url, headers=headers)
        page = urllib2.urlopen(req).read()
        ROOT_PATH = os.getcwd()
        f = open(ROOT_PATH + '/minidou/lib/data/events.txt', 'w')
        dom = html.fromstring(page)
        try:
            page = dom.xpath('//div[@id="db-events-list"]/div[@class="paginator"]/span[@class="thispage"]/@data-total-page')[0]
            #print 'page', page
        except:
            page = 1

        for i in range(1, int(page)):

            url_new = url + "?start=" + str((i - 1) * 10)
            req = urllib2.Request(url_new, headers=headers)
            page = urllib2.urlopen(req).read()
            dom = html.fromstring(page)
            events = dom.xpath('//ul[@class="events-list events-list-pic100 events-list-psmall"]/li')
            for e in events:
                info = e.xpath('div[@class="info"]')[0]
                title = info.xpath('div[@class="title"]/a/span/text()')[0]
                href = info.xpath('div[@class="title"]/a/@href')[0]
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
                re_go_count = re.match(r'^(\d*).*$', counts[0])
                go_count = re_go_count.group(1)
                re_like_count = re.match(r'^(\d*).*$', counts[1])
                like_count = re_like_count.group(1)
                e_list.append({'title': title, 'href': href, 'pic': pic, 'tags': tags, 'etime': etime, 'loc': loc, 'latitude': latitude, 'longtitude': longtitude, 'fee': fee, 'go_count': go_count, 'like_count': like_count})

        for item in e_list:
            f.write("%s\n" % item)

        return [], e_list


class linkQuence:

    def __init__(self):
        self.visted = []
        self.unVisited = []

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

    def addVisitedUrl(self, url):
        """
        get follow urls and save
        """
        self.visted.append(url)

    def removeVisitedUrl(self, url):
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

    def addUnvisitedUrl(self, url):
        """
        deduplicate
        """
        if url != "" and url not in self.visted and url not in self.unVisited:
            self.unVisited.insert(0, url)

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
        return len(self.unVisited) == 0


def movie_crawl(seedid, degree, rtype):
    seedurl = "http://movie.douban.com/subject/" + str(seedid)
    crawl = DoubanCrawler(seedurl)
    crawl.crawl_movie(degree)


def event_crawl(etype, etime):
    etime_l = ["today", "tomorrow", "weekend", "week"]
    etype_l = ["music", "drama", "salon", "party", "film", "exhibition", "sports", "commomwheel", "travel", "all"]
    seedurl = "http://beijing.douban.com/events/" + str(etime_l[int(etime) - 1]) + "-" + str(etype_l[int(etype) - 1])
    crawl = DoubanCrawler(seedurl)
    events = crawl.crawl_event()
    return events


if __name__ == "__main__":
    arg = sys.argv
    #print arg
    if arg[1] == '1':
        logging.info('movie crawl')
        mid = arg[2]
        degree = arg[3]
        rtype = arg[4]
        movie_crawl(mid, degree, rtype)

    if arg[1] == '2':
        logging.info('event crawl')
        etype = arg[2]
        etime = arg[3]
        event_crawl(etype, etime)
