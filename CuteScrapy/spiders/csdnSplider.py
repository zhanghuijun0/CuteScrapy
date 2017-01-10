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


class CsdnSplider(CrawlSpider):
    name = 'blogs.csdn.list'
    custom_settings = {
        'RETRY_TIMES': 50,
        'ITEM_PIPELINES': {
            'CuteScrapy.pipelines.MysqlORMPipeline': 300,
        },
        'DOWNLOAD_TIMEOUT': 120,
        'CONCURRENT_REQUESTS': 5,
        'REACTOR_THREADPOOL_MAXSIZE': 10
    }

    def __init__(self, *args, **kwargs):
        super(CsdnSplider, self).__init__(*args, **kwargs)
        self.commonParser = CommonParser()
        self.blogs = Blogs()
        self.site = 'csdn'

    def start_requests(self):
        yield Request(
            "http://blog.csdn.net/?&page=1",
            meta={'type': 'list', 'page': 1},
            dont_filter=True,
            headers={
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
        )

    def parse(self, response):
        if response.meta['type'] == 'list':
            for item in self.parse_csdn(response):
                yield item

    def parse_csdn(self, response):
        contentlist = response.xpath('//*[@class="blog_list_wrap"]/dl')
        self.logger.info(u'-----------第%s页,%d条数据-----------' % (response.meta['page'], len(contentlist)))
        for item in contentlist:
            page_url = item.xpath('dd/h3/a/@href').extract_first()
            id = hashlib.md5(page_url).hexdigest()
            title = item.xpath('dd/h3/a/text()').extract_first()
            if self.blogs.isExistById(id):
                self.logger.info('title:%s is exist!' % title)
                continue
            summary = item.xpath('dd/div[@class="blog_list_c"]/text()').extract_first()
            dateStr = item.xpath(
                'dd/div[@class="blog_list_b clearfix"]/div[@class="blog_list_b_r fr"]/label/text()').extract_first()
            label = ','.join(item.xpath(
                'dd/div[@class="blog_list_b clearfix"]/div[@class="blog_list_b_l fl"]/span/a//text()').extract())
            blog_url = item.xpath('dt/a[2]/@href').extract_first()
            author = item.xpath('dt/a[2]/text()').extract_first()
            avatar = item.xpath('dt/a/img/@src').extract_first()
            pv = item.xpath(
                'dd/div[@class="blog_list_b clearfix"]/div[@class="blog_list_b_r fr"]/span/em/text()').extract_first()
            positive = item.xpath('dd/div[@class="blog_list_b_b"]/span/em/text()').extract_first()
            blogs = Blogs()
            blogs.id = id
            blogs.site = self.site
            blogs.title = title
            blogs.label = label
            blogs.author = author
            blogs.summary = summary
            blogs.page_url = page_url
            blogs.blog_url = blog_url
            blogs.avatar = avatar
            blogs.pv = pv
            blogs.positive = positive
            blogs.publish_time = parseDateString(dateStr)
            now = datetime.datetime.now()
            blogs.date_update = now.strftime('%Y-%m-%d %H:%M:%S')

            yield ModelItem.getInstance(blogs)
        next_page_url = response.xpath(u'//div[@class="page_nav"]/a[text()="下一页"]/@href').extract_first()
        if next_page_url:
            pageNo = re.search('(\d+)', next_page_url).group(1)
            yield Request(
                'http://blog.csdn.net%s' % next_page_url,
                meta={'type': 'list', 'page': pageNo},
                dont_filter=True,
                headers={
                    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
            )
        else:
            self.logger.info(u'----------CSDN最新博客,一共有%s页----------' % (response.meta['page']))


if __name__ == '__main__':
    execute('scrapy crawl blogs.csdn.list'.split(' '))
