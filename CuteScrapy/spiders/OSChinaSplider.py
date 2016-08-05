# coding:utf8
import random
import re
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.items import CutescrapyItem


class DemoSplider(CrawlSpider):
    name = 'oschina'

    def __init__(self, *args, **kwargs):
        super(DemoSplider, self).__init__(*args, **kwargs)

    def start_requests(self):
        array = range(1, 25)
        while array:
            i = random.choice(array)
            array.remove(i)
            yield Request(
                "http://www.oschina.net/blog?type=0&p=%d" % (i), meta={'type': 'oschina.net'}, dont_filter=True
            )

    def parse(self, response):
        if response.meta['type'] == 'oschina.net':
            for item in self.parse_oschina(response):
                yield item
        else:
            yield

    def parse_oschina(self, response):
        contentlist = response.xpath('//*[@id="RecentBlogs"]/ul[1]/li')
        for item in contentlist:
            article_url = item.xpath('div/h3/a/@href').extract_first()
            article_title = item.xpath('div/h3/a/text()').extract_first()
            brief = item.xpath('div/p/text()').extract_first()
            dateline = item.xpath('div/div/text()').extract_first()
            blog_url = item.xpath('a/@href').extract_first()
            nick_name = dateline.split(' ')[2]
            dateline = dateline.split(' ')[0]

            item = CutescrapyItem()
            item['site'] = response.meta['type']
            item['url'] = article_url
            item['title'] = article_title
            item['label'] = None
            item['brief'] = brief
            item['post_date'] = dateline
            item['blog'] = blog_url
            item['author'] = nick_name
            item['pv'] = None
            item['num_reviews'] = None
            item['diggnum'] = None
            item['burynum'] = None
            yield item


if __name__ == '__main__':
    execute('scrapy crawl oschina'.split(' '))
