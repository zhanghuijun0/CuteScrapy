# coding:utf8
import re
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.items import BlogsItem
from CuteScrapy.resource.ResourceHelper import ResourceHelper


class OsChinaSplider(CrawlSpider):
    name = 'oschina.list'

    def __init__(self, *args, **kwargs):
        super(OsChinaSplider, self).__init__(*args, **kwargs)
        self.site = 'oschina'
        self.resourceHelper = ResourceHelper()
        self.kindList = self.resourceHelper.loadJson('oschina_kinds.json')

    def start_requests(self):
        for item in self.kindList:
            page = 1
            id = item.get('id')
            title = item.get('title')
            url = 'http://www.oschina.net/blog?type=%s&p=%s'
            yield Request(
                url % (id, page),
                meta={'type': 'list', 'page': page, 'id': id, 'title': title, 'url': 'http://www.oschina.net/blog'},
                dont_filter=True,
                headers={
                    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
            )

    def parse(self, response):
        if response.meta['type'] == 'list':
            for item in self.parse_oschina(response):
                yield item
        else:
            yield

    def parse_oschina(self, response):
        contentlist = response.xpath('//*[@id="RecentBlogs"]/ul[1]/li')
        self.logger.info(u'-----------[%s]第%s页,%d条数据-----------' % (
            response.meta['title'], response.meta['page'], len(contentlist)))
        for item in contentlist:
            article_url = item.xpath('div/h3/a/@href').extract_first()
            article_title = item.xpath('div/h3/a/text()').extract_first()
            brief = item.xpath('div/p/text()').extract_first()
            dateline = item.xpath('div/div/text()').extract_first()
            blog_url = item.xpath('a/@href').extract_first()
            nick_name = dateline.split(' ')[0]
            dateline = dateline.split(' ')[2]


            item = BlogsItem()
            item['site'] = self.site
            item['url'] = article_url
            item['title'] = article_title
            item['label'] = response.meta['title']
            item['brief'] = brief.strip() if brief is not None else None
            item['post_date'] = dateline
            item['blog'] = blog_url
            item['author'] = nick_name
            item['pv'] = None
            item['num_reviews'] = None
            item['diggnum'] = None
            item['burynum'] = None
            yield item
        # next_page = response.xpath('//*[@id="RecentBlogs"]/ul[@class="pager"]/li[@class="page next"]/a/@href').extract()
        next_page = response.xpath('//li[@class="page next"]/a/@href').extract_first()
        if next_page:
            page = re.search('p=(\d+)', next_page).group(1)
            url = response.meta['url']
            yield Request(
                url + next_page,
                meta={'type': 'list', 'page': page, 'id': response.meta['id'], 'title': response.meta['title'],
                      'url': url},
                dont_filter=True,
                headers={
                    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
            )


if __name__ == '__main__':
    execute('scrapy crawl oschina.list'.split(' '))
