# coding:utf8
import random
import re
import datetime
import urllib
import urllib2
import requests
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.items import CutescrapyItem
from CuteScrapy.util.DownloadHelper import Download

class DownloadSplider(CrawlSpider):
    name = 'download'

    def __init__(self, *args, **kwargs):
        super(DownloadSplider, self).__init__(*args, **kwargs)
        self.site = 'download'
        self.base = 'http://www.mp4ba.com/'
        self.download = Download()

    def start_requests(self):
        yield Request(
            "http://www.mp4ba.com/show.php?hash=f7edd2ee90e6bf22e12d76c0086323863b26a57d",
            meta={'type': 'list'},
            dont_filter=True
        )

    def parse(self, response):
        if response.status == 200:
            kind = response.xpath('//*[@id="btm"]/div[4]/a/text()').extract()[-1]
            fullname = response.xpath('//*[@id="btm"]/div[4]/text()').extract()[-1].replace('\n', '').replace('\r', '').replace(
                u'»', '').strip()
            name = fullname.split('.')[0]
            url = self.base+response.xpath('//*[@id="download"]/@href').extract_first()
            # self.download.download(url,name)
            print kind
            print name
            print fullname
            print url
            yield




if __name__ == '__main__':
    execute('scrapy crawl download'.split(' '))
