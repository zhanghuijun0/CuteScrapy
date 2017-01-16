# coding:utf8
import hashlib

from scrapy.cmdline import execute
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from CuteScrapy.item.ModelItem import ModelItem
from CuteScrapy.model.applet import Applet
from CuteScrapy.util.CommonParser import CommonParser

__author__ = 'HuijunZhang'


# 微信小程序爬取(小程序窝)
class XcxwoSplider(CrawlSpider):
    name = 'applet.xcxwo'
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
        super(XcxwoSplider, self).__init__(*args, **kwargs)
        self.commonParser = CommonParser()
        self.applet = Applet()
        self.site = 'xcxwo'

    def start_requests(self):
        yield FormRequest(
            "http://www.xcxwo.com/app/appList",
            formdata={
                "ckey": '',
                "page": '1',
                "q": ''
            },
            meta={'type': 'list', 'page_no': 1},
            dont_filter=True
        )

    def parse(self, response):
        if not response.body_as_unicode():
            self.logger.info(u'一共%s页,没有了!' % (response.meta['page_no'] - 1))
            return
        if response.meta['type'] == 'list':
            for item in self.parse_list(response):
                yield item
        elif response.meta['type'] == 'detail':
            for item in self.parse_detail(response):
                yield item

    def parse_list(self, response):
        for item in response.xpath('//body/div/a'):
            url = item.xpath('@href').extract_first()
            # id = url.split('/')[-1]
            icon = item.xpath('div[@class="header"]/img/@src').extract_first()
            name = item.xpath('div[@class="header"]/div[@class="title left"]/h1/text()').extract_first()
            author = self.commonParser.trim(item.xpath('div[@class="header"]/div[@class="title left"]/p/text()').extract_first().replace(u'发布者：',''))
            id = hashlib.md5((u'%s%s%s' % (self.site, name, author)).encode("utf8")).hexdigest()
            label = ','.join(item.xpath('div[@class="cate"]/span/text()').extract())
            star = len(item.xpath(
                'div[@class="i-footer"]/div[@class="stars left"]/i[@class="fa fa-star star-active"]').extract())
            heart_share = item.xpath('div[@class="i-footer"]/div[@class="right"]/text()').extract()
            heart = heart_share[1].replace(' ', '')
            share = heart_share[2].replace(' ', '')
            qrcode = item.xpath('div[@class="qrcodeTooltip"]/img/@src').extract_first()
            applet = Applet()
            applet.id = id
            applet.site = self.site
            applet.name = name
            applet.author = author
            applet.label = label
            applet.star = star
            applet.heart = heart
            applet.share = share
            applet.page_url = 'http://www.xcxwo.com%s' % url
            applet.icon = icon
            applet.qrcode = qrcode
            if not self.applet.isExistById(id):
                yield Request(
                    'http://www.xcxwo.com%s' % url,
                    meta={'type': 'detail', 'applet': applet},
                    dont_filter=True
                )
            else:
                self.logger.info('id:%s is exists' % id)
                yield ModelItem.getInstance(applet)
        yield FormRequest(
            "http://www.xcxwo.com/app/appList",
            formdata={
                "ckey": '',
                "page": str(response.meta['page_no'] + 1),
                "q": ''
            },
            meta={'type': 'list', 'page_no': response.meta['page_no'] + 1},
            dont_filter=True
        )

    def parse_detail(self, response):
        applet = response.meta['applet']
        applet.pictures = ','.join(response.xpath('//table[@class="table"]/tr/td/div/a/@href').extract())
        applet.summary = self.commonParser.trim(
            response.xpath('//span[@class="app-description"]/text()').extract_first())
        applet.publish_time = response.xpath('//span[@class="app-info-item"]/text()').extract_first()
        yield ModelItem.getInstance(applet)


if __name__ == '__main__':
    execute('scrapy crawl applet.xcxwo'.split(' '))
