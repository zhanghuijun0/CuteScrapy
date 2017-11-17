# coding:utf8
import hashlib
import json
import urllib

import re

import datetime
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.item.ModelItem import ModelItem
from CuteScrapy.model.news import News
from CuteScrapy.util.CommonParser import CommonParser
from CuteScrapy.util.date import timestamp2datetime

__author__ = 'HuijunZhang'


# 查询ip地址
class IPSplider(CrawlSpider):
    name = 'ip.check'
    custom_settings = {
        'RETRY_TIMES': 50,
        'ITEM_PIPELINES': {
            'CuteScrapy.pipelines.MysqlORMPipeline': 300
        },
        'DOWNLOADER_MIDDLEWARES': {
            'CuteScrapy.middlewares.RandomProxyMiddleware': 800,
            'CuteScrapy.middlewares.UserAgentMiddleware': 600
        },
        'DOWNLOAD_TIMEOUT': 120,
        'CONCURRENT_REQUESTS': 5,
        'REACTOR_THREADPOOL_MAXSIZE': 10
    }

    def __init__(self, *args, **kwargs):
        super(IPSplider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield Request(
            'http://www.baidu.com/s?wd=ip',
            dont_filter=True
        )

    def parse(self, response):
        result = ''.join(response.xpath(
            '//img[@src="//www.baidu.com/aladdin/img/tools/ip.png"]/../following-sibling::*[1]//text()').extract()).strip()
        print result
        yield None


if __name__ == '__main__':
    execute('scrapy crawl ip.check'.split(' '))
