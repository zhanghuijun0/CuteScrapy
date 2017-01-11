# coding:utf8
import hashlib
import re
import datetime
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.item.ModelItem import ModelItem
from CuteScrapy.model.blogs import Blogs
from CuteScrapy.util.CommonParser import CommonParser
from CuteScrapy.util.date import parseDateString

__author__ = 'HuijunZhang'

class BlogsSplider(CrawlSpider):
    name = 'blogs.cnblogs.list'
    custom_settings = {
        'RETRY_TIMES': 50,
        'ITEM_PIPELINES': {
            'CuteScrapy.pipelines.MysqlORMPipeline': 300,
            # 'CuteScrapy.pipelines.JsonWriterPipeline': 350,
        },
        'DOWNLOAD_TIMEOUT': 120,
        'CONCURRENT_REQUESTS': 5,
        'REACTOR_THREADPOOL_MAXSIZE': 10
    }

    def __init__(self, *args, **kwargs):
        super(BlogsSplider, self).__init__(*args, **kwargs)
        self.commonParser = CommonParser()
        self.blogs = Blogs()
        self.site = 'cnblogs'

    def start_requests(self):
        for i in range(200, 0, -1):
            yield Request(
                "http://www.cnblogs.com/sitehome/p/%d" % (i),
                meta={'type': 'list'},
                dont_filter=True
            )

    def parse(self, response):
        if response.status == 200:
            if response.meta['type'] == 'list':
                for item in self.parse_blogs(response):
                    yield item

    def parse_blogs(self, response):
        for item in response.xpath('//*[@id="post_list"]/div'):
            page_url = item.xpath('div[@class="post_item_body"]/h3/a/@href').extract_first()
            id = hashlib.md5(page_url).hexdigest()
            title = item.xpath('div[@class="post_item_body"]/h3/a/text()').extract_first()
            if self.blogs.isExistById(id):
                self.logger.info('id:%s is exist!' % id)
                continue
            author = item.xpath('div/div[@class="post_item_foot"]/a/text()').extract_first()
            avatar = item.xpath('div[@class="post_item_body"]/p/a/img/@src').extract_first()
            blog_url = item.xpath('div/div[@class="post_item_foot"]/a/@href').extract_first()
            summary = self.commonParser.trim(''.join(item.xpath('div[@class="post_item_body"]/p/text()').extract()))
            dateStr = self.commonParser.trim(''.join(item.xpath('div[@class="post_item_body"]/div/text()').extract()))
            pv = item.xpath('div[2]/div/span[2]/a/text()').extract_first().strip()
            cv = item.xpath('div[2]/div/span[1]/a/text()').extract_first().strip()
            positive = item.xpath('div[1]/div[1]/span/text()').extract_first()
            pv = re.findall(r'\d+', pv)[0]
            cv = re.findall(r'\d+', cv)[0]

            blogs = Blogs()
            blogs.id = id
            blogs.site = self.site
            blogs.title = title
            blogs.label = None
            blogs.author = author
            blogs.summary = summary
            blogs.content = None
            blogs.avatar = avatar
            blogs.page_url = page_url
            blogs.blog_url = blog_url
            blogs.pv = pv
            blogs.cv = cv
            blogs.positive = positive
            blogs.publish_time = parseDateString(dateStr)
            blogs.date_update = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield ModelItem.getInstance(blogs)



if __name__ == '__main__':
    execute('scrapy crawl blogs.cnblogs.list'.split(' '))
