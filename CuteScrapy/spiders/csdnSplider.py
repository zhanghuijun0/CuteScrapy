# coding:utf8
import re
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.items import CutescrapyItem


class CsdnSplider(CrawlSpider):
    name = 'csdn.list'

    def __init__(self, *args, **kwargs):
        super(CsdnSplider, self).__init__(*args, **kwargs)
        self.site = 'csdn'
        self.url = 'http://blog.csdn.net'

    def start_requests(self):
        yield Request(
            "http://blog.csdn.net/?&page=1", meta={'type': 'list', 'page': 1}, dont_filter=True
        )

    def parse(self, response):
        if response.meta['type'] == 'list':
            for item in self.parse_csdn(response):
                yield item
        else:
            yield

    def parse_csdn(self, response):
        contentlist = response.xpath('//*[@class="blog_list_wrap"]/dl')
        self.logger.info(u'-----------第%s页,%d条数据-----------' % (response.meta['page'], len(contentlist)))
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
            item['site'] = self.site
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
        if response.xpath('//*[@class="page_nav"]/a/text()').extract()[-2] == u'下一页':
            next_url = response.xpath('//*[@class="page_nav"]/a/@href').extract()[-2]
            pageNo = re.search('(\d+)', next_url).group(1)
            url = self.url + next_url
            yield Request(
                url, meta={'type': 'list', 'page': pageNo}, dont_filter=True
            )
        else:
            self.logger.info(u'----------CSDN最新博客,一共有%s页----------' % (response.meta['page']))


if __name__ == '__main__':
    execute('scrapy crawl csdn.list'.split(' '))
