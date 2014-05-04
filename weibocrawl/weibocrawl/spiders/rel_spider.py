from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from ..login import login
# from ..items import relItem



class weiboSpider(CrawlSpider):
    http_user = 'starrydai@sina.com'
    http_pass = 'dairui1130'
    name = "rel"
    allowed_domains = []
    # '''
    # impersonate login
    # '''
    # username = 'starrydai@sina.com'
    # pwd = 'dairui1130'
    # cookie_file = 'weibo_login_cookies.dat'
    # lg = login()
    # if lg.login(username, pwd, cookie_file):
    #     print 'Login WEIBO succeeded'
    # else:
    #     print 'login failure'

    start_urls = ["http://weibo.com/p/1005051087306505"]
    # for e in g_:
    #     start_urls.append('http://www.last.fm/user/' + e.strip() + '/friends')


    def parse(self, response):
        self.log('Hi, this is: %s' % response.url)


        # '''
        # impersonate login
        # '''
        # username = 'starrydai@sina.com'
        # pwd = 'dairui1130'
        # cookie_file = 'weibo_login_cookies.dat'
        # if login.login(username, pwd, cookie_file):
        #     print 'Login WEIBO succeeded'
        # else:
        #     print 'login failure'

        # self.log('Hi, this is: %s' % response.url)
        # hxs = HtmlXPathSelector(response)
        # sites = hxs.select('//div[@class="userContainer"]/div/strong/a/text()').extract()
        # # pname = (hxs.select('//span[@class = "nickname"]/text()').extract())[0].decode('utf-8')
        #
        # try:
        #     try:
        #         page = int(hxs.select('//a[@class = "pagelink lastpage"]/text()').extract()[0])
        #         print page
        #     except:
        #         page = int(hxs.select('//span[@class = "selected"]/text()').extract()[0])
        #         print page
        # except:
        #     page = 1
        #     print 'ex',page
        #
        #
        #
        # name = self.get_username(response.url)
        # print self.get_username(response.url)
        # for site in sites:
        #
        #     print site
        # yield item
        #
        #
        # for p in range(1, page):
        #     url = 'http://cn.last.fm/user/' + name + '/friends?page=' + str(p)
        #     yield Request(url, callback=self.parse)


