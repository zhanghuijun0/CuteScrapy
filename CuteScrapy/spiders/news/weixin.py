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


# 资讯(微信)
class MinappSplider(CrawlSpider):
    name = 'news.weixin'
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
        'CONCURRENT_REQUESTS': 5,
        'REACTOR_THREADPOOL_MAXSIZE': 10
    }

    def __init__(self, *args, **kwargs):
        super(MinappSplider, self).__init__(*args, **kwargs)
        self.commonParser = CommonParser()
        self.news = News()
        self.site = 'minapp'

    def start_requests(self):
        for key in [u'余额宝',u'金岩财富网']:
            url = 'http://weixin.sogou.com/weixin?type=2&query=%s&ie=utf8&_sug_=n&_sug_type_&page=%s&tsn=2' % (key, 1)
            yield Request(
                url,
                meta={'type': 'list', 'keywords': key, 'sentiment': False, 'page_no': 1},
                dont_filter=True
            )

    def parse(self, response):
        if response.status == 200:
            if response.meta['type'] == 'list':
                for item in self.parse_list(response):
                    yield item
            elif response.meta['type'] == 'detail':
                opinion = response.meta['opinion']
                opinion.page_url = response.url
                yield ModelItem.getInstance(opinion)

    def parse_list(self, response):
        keywords = response.meta['keywords']
        page_no = response.meta['page_no']
        self.logger.info('keydords:%s,page_no:%s' % (keywords, page_no))
        next_page = False
        for item in response.xpath('//ul[@class="news-list"]/li'):
            try:
                page_url = item.xpath('div/h3/a/@href').extract_first()
                title = ''.join(item.xpath('div/h3/a//text()').extract())
                publish_time_stamp = item.xpath('div/div/span/script').extract_first()
                publish_time = timestamp2datetime(int(re.search('(\d{10})', publish_time_stamp).group(1)))
                summary = ''.join(item.xpath('div/p//text()').extract())
                account = item.xpath('div/div/a/text()').extract_first()  # 公众号
                if title.find(keywords) > -1 or summary.find(keywords) > -1:
                    next_page = True
                else:
                    next_page = False
                    continue
                id = hashlib.md5((publish_time_stamp + title).encode('utf8')).hexdigest()
                if self.news.isExistById(id):
                    self.logger.info('title:%s is exist!' % title)
                    continue
                opinion = News()
                opinion.id = id
                opinion.site = self.site
                opinion.title = u'%s   ——%s' % (title, account)
                opinion.keyword = keywords
                opinion.summary = self.commonParser.replaceSpace(summary)
                # if response.meta['sentiment'] and opinion.content != None and opinion.content != '':
                #     list = self.commonParser.getBosonNLP(opinion.content)
                #     opinion.positive = list[0][0]
                #     opinion.negative = list[0][1]
                opinion.page_url = page_url
                opinion.status = 0
                opinion.publish_time = publish_time
                opinion.comment_time = publish_time
                now = datetime.datetime.now()
                opinion.date_create = now.strftime('%Y-%m-%d %H:%M:%S')
                yield Request(
                    page_url + '&pass_ticket=qMx7ntinAtmqhVn+C23mCuwc9ZRyUp20kIusGgbFLi0=&uin=MTc1MDA1NjU1&ascene=1',
                    meta={'type': 'detail', 'opinion': opinion, 'url': page_url},
                    dont_filter=True
                )
            except Exception as e:
                self.logger.error(e)
        if next_page:
            next_page_no = response.meta['page_no'] + 1
            yield Request(
                url='http://weixin.sogou.com/weixin?type=2&query=%s&ie=utf8&_sug_=n&_sug_type_&page=%s&tsn=2' % (
                    keywords, next_page_no),
                meta={'type': 'list', 'keywords': keywords, 'sentiment': response.meta['sentiment'],
                      'page_no': next_page_no},
                dont_filter=True
            )

    def close(self, reason):
        pass


if __name__ == '__main__':
    execute('scrapy crawl news.weixin'.split(' '))
