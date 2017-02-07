# coding:utf8
import hashlib
import json
import urllib
import re
import datetime

import sys
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.item.ModelItem import ModelItem
from CuteScrapy.model.news import News
from CuteScrapy.resource.ResourceHelper import ResourceHelper
from CuteScrapy.util.CommonParser import CommonParser
from CuteScrapy.util.date import timestamp2datetime

__author__ = 'HuijunZhang'


# 小说(落霞小说)
class LuoxiaSplider(CrawlSpider):
    name = 'novel.luoxia'
    custom_settings = {
        'RETRY_TIMES': 50,
        'ITEM_PIPELINES': {
            'CuteScrapy.pipelines.MysqlORMPipeline': 300
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'CuteScrapy.middlewares.RandomProxyMiddleware': 800,
            'CuteScrapy.middlewares.UserAgentMiddleware': 600
        },
        'DOWNLOAD_TIMEOUT': 120,
        'CONCURRENT_REQUESTS': 1,
        'REACTOR_THREADPOOL_MAXSIZE': 10
    }

    def __init__(self, *args, **kwargs):
        super(LuoxiaSplider, self).__init__(*args, **kwargs)
        reload(sys)
        sys.setdefaultencoding("utf-8")
        self.site = 'luoxia'
        self.content = []
        self.resourceHelper = ResourceHelper()

    def start_requests(self):
        list = [
            # {'title': u'第一部 精绝古城', 'url': 'http://www.luoxia.com/guichui/gcd-1/'},
            # {'title': u'第二部 龙岭迷窟', 'url': 'http://www.luoxia.com/guichui/gcd-2/'},
            # {'title': u'第三部 云南虫谷', 'url': 'http://www.luoxia.com/guichui/gcd-3/'},
            # {'title': u'第四部 昆仑神宫', 'url': 'http://www.luoxia.com/guichui/gcd-4/'},
            # {'title': u'第五部 黄皮子坟', 'url': 'http://www.luoxia.com/guichui/gcd-5/'},
            # {'title': u'第六部 南海归墟', 'url': 'http://www.luoxia.com/guichui/gcd-6/'},
            # {'title': u'第七部 怒晴湘西', 'url': 'http://www.luoxia.com/guichui/gcd-7/'},
            # {'title': u'第八部 巫峡棺山', 'url': 'http://www.luoxia.com/guichui/gcd-8/'},
            {'title': u'鬼吹灯之牧野诡事', 'url': 'http://www.luoxia.com/guichui/gcd-mygs/'},
            {'title': u'鬼吹灯之圣泉寻踪', 'url': 'http://www.luoxia.com/guichui/gcd-sqxz/'},
            {'title': u'鬼吹灯之抚仙毒蛊', 'url': 'http://www.luoxia.com/guichui/gcd-fxdg/'},
            {'title': u'鬼吹灯之山海妖冢', 'url': 'http://www.luoxia.com/guichui/gcd-shyz/'},
            {'title': u'鬼吹灯之湘西疑陵', 'url': 'http://www.luoxia.com/guichui/gcd-xxyl/'},
            {'title': u'鬼吹灯之镇库狂沙', 'url': 'http://www.luoxia.com/guichui/gcd-zkks/'}
        ]
        for item in list:
            yield Request(
                item.get('url'),
                meta={'type': 'list', 'title': u'%s.txt' % item.get('title')},
                dont_filter=True
            )

    def parse(self, response):
        if response.status == 200:
            if response.meta['type'] == 'list':
                for item in self.parse_list(response):
                    yield item
            elif response.meta['type'] == 'detail':
                for item in self.parse_detail(response):
                    yield item

    def parse_list(self, response):
        url = response.xpath('//div[@class="book-list clearfix"]/ul/li/a/@href').extract_first()
        yield Request(
            url,
            meta={'type': 'detail', 'title': response.meta['title'], 'count': 1},
            dont_filter=True
        )

    def parse_detail(self, response):
        title2 = response.xpath('//h1[@class="post-title"]/text()').extract_first()
        content = '\n\t'.join(response.xpath('//article/p/text()').extract())
        text = '%s\n\t%s\n\n' % (title2, content)
        self.content.append(text.encode('utf-8'))
        self.resourceHelper.append(response.meta['title'], text)
        self.logger.info('%s,%s' % (response.meta['title'], title2))
        next_page_url = response.xpath(u'//li[text()="下一章："]/a/@href').extract_first()
        next_title = response.xpath(u'//li[text()="下一章："]/a/text()').extract_first()
        if response.meta['count'] > 5 and next_title.find(u'第一章') > -1:
            self.logger.info(u'-----%s 已完结-----' % response.meta['title'])
            return
        yield Request(
            next_page_url,
            meta={'type': 'detail', 'title': response.meta['title'], 'count': response.meta['count'] + 1},
            dont_filter=True
        )


if __name__ == '__main__':
    execute('scrapy crawl novel.luoxia'.split(' '))
