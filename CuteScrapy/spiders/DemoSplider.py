# coding:utf8
import random
import re
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.items import CutescrapyItem


class DemoSplider(CrawlSpider):
    name = 'demo'

    # allowed_domains = ['blogs.com']
    # start_urls = [
    #     "http://www.cnblogs.com/#p1",
    #     "http://blog.csdn.net/?&page=1"
    # ]


    def __init__(self, *args, **kwargs):
        super(DemoSplider, self).__init__(*args, **kwargs)

    def start_requests(self):
        array = range(1, 5)
        while array:
            i = random.choice(array)
            array.remove(i)
            yield Request(
                "http://blog.csdn.net/?&page=%d" % (i), meta={'type': 'csdn.net'}, dont_filter=True
            )
            # yield Request(
            #     "http://www.cnblogs.com/sitehome/p/%d" % (i),meta={'type':'cnblogs.com'}, dont_filter = True
            # )

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
            # label = item.xpath('dd/div[2]/div[1]/span/a/text()').extract_first()
            blog_url = item.xpath('dt/a[2]/@href').extract_first()
            nick_name = item.xpath('dt/a[2]/text()').extract_first()
            label = item.xpath('dd/div[2]/div[2]/span/em/text()').extract_first()

            item = CutescrapyItem()
            item['blog_type'] = response.meta['type']
            item['article_url'] = article_url
            item['article_title'] = article_title
            item['brief'] = brief
            item['dateline'] = dateline
            item['blog_url'] = blog_url
            item['nick_name'] = nick_name
            item['label'] = label
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
            dateline = re.findall(r'\d+-\d+-\d+\s*\d+\:\d+', dateline)[0]

            item = CutescrapyItem()
            item['blog_type'] = response.meta['type']
            item['article_url'] = article_url
            item['article_title'] = article_title
            item['brief'] = brief
            item['dateline'] = dateline
            item['blog_url'] = blog_url
            item['nick_name'] = nick_name
            item['label'] = None
            yield item

    def writeMetaFile(self, response):
        filename = response.url.split("/")[-1]
        print filename
        if 'htm' not in filename:
            filename = filename + '.html'
        with open('../../files/' + filename, 'wb') as f:
            f.write(response.body.replace('charset=gb2312', 'charset=utf8'))


if __name__ == '__main__':
    execute('scrapy crawl demo'.split(' '))
