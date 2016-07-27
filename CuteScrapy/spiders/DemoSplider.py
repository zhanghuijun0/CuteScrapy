# coding:utf8
import random
import re
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.items import CutescrapyItem


class DemoSplider(CrawlSpider):
    name = 'demo'

    def __init__(self, *args, **kwargs):
        super(DemoSplider, self).__init__(*args, **kwargs)

    def start_requests(self):
        array = range(1, 200)
        while array:
            i = random.choice(array)
            array.remove(i)
            yield Request(
                "http://blog.csdn.net/?&page=%d" % (i), meta={'type': 'csdn.net'}, dont_filter=True
            )
            yield Request(
                "http://www.cnblogs.com/sitehome/p/%d" % (i), meta={'type': 'cnblogs.com'}, dont_filter=True
            )

    def parse(self, response):
        if response.meta['type'] == 'cnblogs.com':
            for item in self.parse_blogs(response):
                yield item
        elif response.meta['type'] == 'csdn.net':
            for item in self.parse_csdn(response):
                yield item
        else:
            yield

    def parse_csdn(self, response):
        contentlist = response.xpath('/html/body/div[3]/div[1]/div[3]/dl')
        for item in contentlist:
            article_url = item.xpath('dd/h3/a/@href').extract_first()
            article_title = item.xpath('dd/h3/a/text()').extract_first()
            brief = item.xpath('dd/div[1]/text()').extract_first().strip()
            dateline = item.xpath('dd/div[2]/div[2]/label/text()').extract_first()
            label = item.xpath('dd/div[2]/div[1]/span/a/text()').extract_first()
            blog_url = item.xpath('dt/a[2]/@href').extract_first()
            nick_name = item.xpath('dt/a[2]/text()').extract_first()
            pv = item.xpath('dd/div[2]/div[2]/span/em/text()').extract_first()

            item = CutescrapyItem()
            item['site'] = response.meta['type']
            item['url'] = article_url
            item['title'] = article_title
            item['label'] = label
            item['brief'] = brief
            item['post_date'] = dateline
            item['blog'] = blog_url
            item['author'] = nick_name
            item['pv'] = pv
            item['num_reviews'] = None
            item['diggnum'] = None
            item['burynum'] = None
            yield item

    def parse_blogs(self, response):
        contentlist = response.xpath('//*[@id="post_list"]/div')
        for item in contentlist:
            article_url = item.xpath('div[2]/h3/a/@href').extract_first()
            article_title = item.xpath('div[2]/h3/a/text()').extract_first()
            brief = item.xpath('div[2]/p/text()').extract()[0].strip()
            dateline = item.xpath('div[2]/div/text()').extract()[1].strip()
            blog_url = item.xpath('div[2]/div/a/@href').extract_first()
            nick_name = item.xpath('div[2]/div/a/text()').extract_first()
            pv = item.xpath('div[2]/div/span[2]/a/text()').extract_first().strip()
            num_reviews = item.xpath('div[2]/div/span[1]/a/text()').extract_first().strip()
            diggnum = item.xpath('div[1]/div[1]/span/text()').extract_first()
            dateline = re.findall(r'\d+-\d+-\d+\s*\d+\:\d+', dateline)[0]
            pv = re.findall(r'\d+', pv)[0]
            num_reviews = re.findall(r'\d+', num_reviews)[0]

            item = CutescrapyItem()
            item['site'] = response.meta['type']
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
            yield item

    def writeMetaFile(self, response):
        filename = response.url.split("/")[-1]
        print filename
        if 'htm' not in filename:
            filename = filename + '.html'
        with open('../files/' + filename, 'wb') as f:
            f.write(response.body.replace('charset=gb2312', 'charset=utf8'))


if __name__ == '__main__':
    execute('scrapy crawl demo'.split(' '))
