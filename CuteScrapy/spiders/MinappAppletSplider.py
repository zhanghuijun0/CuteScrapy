# coding:utf8
import json
from scrapy.cmdline import execute
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from CuteScrapy.item.ModelItem import ModelItem
from CuteScrapy.model.applet import Applet
from CuteScrapy.util.CommonParser import CommonParser
from CuteScrapy.util.date import timestamp2datetime

__author__ = 'HuijunZhang'


# 微信小程序爬取(知晓)
class MinappSplider(CrawlSpider):
    name = 'applet.minapp'
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
        self.applet = Applet()
        self.site = 'minapp'

    def start_requests(self):
        yield Request(
            'https://minapp.com/api/v3/trochili/miniapp/?limit=21',
            meta={'type': 'list', 'page_no': 1},
            dont_filter=True
        )

    def parse(self, response):
        if response.meta['type'] == 'list':
            for item in self.parse_list(response):
                yield item
        elif response.meta['type'] == 'share':
            for item in self.parse_share_vote(response):
                yield item

    def parse_list(self, response):
        body = json.loads(response.body_as_unicode())
        if response.meta['page_no'] == 1:
            total_count = body.get('meta').get('total_count')
            self.logger.info('total_count:%s' % total_count)
        id_list = []
        for item in body.get('objects'):
            id_list.append(str(item.get('id')))
            id = '%s_%s' % (self.site, item.get('id'))
            name = item.get('name')
            author = item.get('created_by')
            label = []
            for tag in item.get('tag'):
                label.append(tag.get('name'))
            label = ','.join(label)
            summary = item.get('description')
            star = item.get('overall_rating')
            page_url = 'https://minapp.com/miniapp/%s/' % item.get('id')
            icon = item.get('icon').get('image')
            qrcode = item.get('qrcode').get('image')
            pictures = []
            for screenshot in item.get('screenshot'):
                pictures.append(screenshot.get('image'))
            pictures = ','.join(pictures)
            publish_time = timestamp2datetime(item.get('created_at'))
            applet = Applet()
            applet.id = id
            applet.site = self.site
            applet.name = name
            applet.author = author
            applet.label = label
            applet.summary = summary
            applet.star = star
            # applet.heart = heart
            # applet.share = share
            applet.page_url = page_url
            applet.icon = icon
            applet.qrcode = qrcode
            applet.pictures = pictures
            applet.summary = summary
            applet.publish_time = publish_time
            yield ModelItem.getInstance(applet)
        id_in = ','.join(id_list)
        yield Request(
            'https://minapp.com/api/v3/trochili/miniapp/stat/?id__in=%s&limit=%s' % (id_in, len(id_in)),
            meta={'type': 'share', 'page_no': response.meta['page_no']},
            dont_filter=True
        )
        if not body.get('meta').get('next'):
            self.logger.info(u'最后一页:%s,一共%s个App' % (response.meta['page_no'], body.get('meta').get('total_count')))
        else:
            yield Request(
                'https://minapp.com%s' % body.get('meta').get('next'),
                meta={'type': 'list', 'page_no': response.meta['page_no']},
                dont_filter=True
            )

    def parse_share_vote(self, response):
        body = json.loads(response.body_as_unicode())
        for item in body.get('objects'):
            id = '%s_%s' % (self.site, item.get('id'))
            share_count = item.get('share_count')
            vote_count = item.get('vote_count')
            applet = Applet()
            applet.id = id
            applet.site = self.site
            applet.share = share_count
            applet.heart = vote_count
            yield ModelItem.getInstance(applet)


if __name__ == '__main__':
    execute('scrapy crawl applet.minapp'.split(' '))
