# Scrapy settings for weibocrawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'weibocrawl'

SPIDER_MODULES = ['weibocrawl.spiders']
NEWSPIDER_MODULE = 'weibocrawl.spiders'

ITEM_PIPELINES = [
    "weibocrawl.pipelines.WeibocrawlPipeline",
]


#cookies
COOKIES_ENABLED = True
COOKIES_DEBUG = True


#bfo
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'


SCHEDULER_MIDDLEWARES = {
    'scheduler_middlewares.DuplicatesFilterMiddleware': 500
}

DOWNLOADER_MIDDLEWARES = {
    'weibocrawl.middlewares.CustomDownloaderMiddleware': 543,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weibocrawl (+http://www.yourdomain.com)'
