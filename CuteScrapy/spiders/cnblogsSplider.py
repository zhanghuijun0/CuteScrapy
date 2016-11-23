# coding:utf8
import random
import re
import datetime
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.items import BlogsItem


class BlogsSplider(CrawlSpider):
    name = 'cnblogs.list'

    def __init__(self, *args, **kwargs):
        super(BlogsSplider, self).__init__(*args, **kwargs)
        self.site = 'cnblogs'

    def start_requests(self):
        array = range(1, 200)
        while array:
            i = random.choice(array)
            array.remove(i)
            yield Request(
                "http://www.cnblogs.com/sitehome/p/%d" % (i), meta={'type': 'list'}, dont_filter=True
            )

    def parse(self, response):
        if response.status == 200:
            if response.meta['type'] == 'list':
                for item in self.parse_blogs(response):
                    yield item
            else:
                yield

    def parse_blogs(self, response):
        contentlist = response.xpath('//*[@id="post_list"]/div')
        for item in contentlist:
            article_url = item.xpath('div[2]/h3/a/@href').extract_first()
            article_title = item.xpath('div[2]/h3/a/text()').extract_first()
            brief = item.xpath('div[2]/p/text()').extract()[-1].strip()
            dateline = item.xpath('div[2]/div/text()').extract()[1].strip()
            blog_url = item.xpath('div[2]/div/a/@href').extract_first()
            nick_name = item.xpath('div[2]/div/a/text()').extract_first()
            pv = item.xpath('div[2]/div/span[2]/a/text()').extract_first().strip()
            num_reviews = item.xpath('div[2]/div/span[1]/a/text()').extract_first().strip()
            diggnum = item.xpath('div[1]/div[1]/span/text()').extract_first()
            dateline = re.findall(r'\d+-\d+-\d+\s*\d+\:\d+', dateline)[0]
            pv = re.findall(r'\d+', pv)[0]
            num_reviews = re.findall(r'\d+', num_reviews)[0]
            self.logger.info('title:'+article_title)
            item = BlogsItem()
            item['site'] = self.site
            item['url'] = article_url
            item['title'] = article_title
            item['label'] = None
            item['brief'] = brief
            item['post_date'] = dateline
            item['blog'] = blog_url
            item['author'] = nick_name
            item['pv'] = pv
            item['num_reviews'] = num_reviews
            item['diggnum'] = diggnum
            item['burynum'] = None
            item['date_update'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item


if __name__ == '__main__':
    execute('scrapy crawl cnblogs.list'.split(' '))
