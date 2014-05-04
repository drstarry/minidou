from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from ..items import weiboItem


class weiboSpider(CrawlSpider):
    name = "weibo"
    allowed_domains = []

    start_urls = []
    # for e in g_:
    #     start_urls.append('http://www.last.fm/user/' + e.strip() + '/friends')


    def parse(self, response):
        pass
    #     self.log('Hi, this is: %s' % response.url)
    #     hxs = HtmlXPathSelector(response)
    #     sites = hxs.select('//div[@class="userContainer"]/div/strong/a/text()').extract()
    #     # pname = (hxs.select('//span[@class = "nickname"]/text()').extract())[0].decode('utf-8')
    #
    #     try:
    #         try:
    #             page = int(hxs.select('//a[@class = "pagelink lastpage"]/text()').extract()[0])
    #             print page
    #         except:
    #             page = int(hxs.select('//span[@class = "selected"]/text()').extract()[0])
    #             print page
    #     except:
    #         page = 1
    #         print 'ex',page
    #
    #
    #
    #     name = self.get_username(response.url)
    #     print self.get_username(response.url)
    #     for site in sites:
    #
    #         print site
    #     yield item
    #
    #
    #     for p in range(1, page):
    #         url = 'http://cn.last.fm/user/' + name + '/friends?page=' + str(p)
    #         yield Request(url, callback=self.parse)
    #
    #
    # def get_username(self, url):
    #     find_index = url.find("cn.last.fm/user/")
    #     if find_index >= 0:
    #         x = url[find_index:].split("/")
    #         return x[2]
    #     return None