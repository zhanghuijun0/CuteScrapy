# coding:utf8
import re
import traceback
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.items import BlogsItem
from CuteScrapy.resource.ResourceHelper import ResourceHelper


class OsChinaSplider(CrawlSpider):
    name = 'blogs.oschina'

    def __init__(self, *args, **kwargs):
        super(OsChinaSplider, self).__init__(*args, **kwargs)
        self.site = 'oschina'
        self.resourceHelper = ResourceHelper()
        self.kindList = self.resourceHelper.loadJson('oschina_kinds.json')

    def start_requests(self):
        for item in self.kindList:
            classification = item.get('id')
            label = item.get('title')
            yield Request(
                'https://www.oschina.net/action/ajax/get_more_recommend_blog?classification=%s&p=%s' % (
                    classification, 1),
                meta={'type': 'list', 'page_no': 1, 'classification': classification, 'label': label},
                dont_filter=True,
                headers={
                    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
            )

    def parse(self, response):
        if response.meta['type'] == 'list':
            for item in self.parse_oschina(response):
                yield item

    def parse_oschina(self, response):
        list = response.xpath('//body/div')
        for sec in list:
            try:
                item = BlogsItem()
                item['site'] = self.site
                item['url'] = sec.xpath('div[@class="box-fl"]/a/@href').extract_first()
                item['title'] = sec.xpath('div[@class="box-aw"]/header/a/@title').extract_first()
                item['label'] = response.meta['label']
                item['brief'] = sec.xpath('div[@class="box-aw"]/section/text()').extract_first()
                item['post_date'] = sec.xpath('div[@class="box-aw"]/footer/span/text()').extract()[2]
                item['blog'] = sec.xpath('div[@class="box-aw"]/header/a/@href').extract_first()
                item['author'] = sec.xpath('div[@class="box-fl"]/a/img/@alt').extract_first()
                footer = sec.xpath('div[@class="box-aw"]/footer').extract_first()
                pv = re.search(u'阅读 (\d+)', footer)
                num_reviews = re.search(u'评论 (\d+)', footer)
                diggnum = re.search(u'点赞 (\d+)', footer)
                item['pv'] = pv.group(1) if pv else None
                item['num_reviews'] = num_reviews.group(1) if num_reviews else None
                item['diggnum'] = diggnum.group(1) if diggnum else None
                item['burynum'] = None
                self.logger.info('title:%s' % item['title'])
                yield item
            except Exception as e:
                traceback.print_exc()
                self.logger.error(e)
        next_page = response.xpath('//body/a/@href').extract_first()
        if next_page:
            next_page_no = re.search('p=(\d+)', next_page).group(1)
            yield Request(
                'https://www.oschina.net%s' % (next_page),
                meta={'type': 'list', 'page_no': next_page_no, 'classification': response.meta['classification'],
                      'label': response.meta['label']},
                dont_filter=True,
                headers={
                    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
            )
        else:
            self.logger.info(
                'page_no:%s,msg:%s' % (response.meta['page_no'], response.xpath('//body/p/text()').extract_first()))


if __name__ == '__main__':
    execute('scrapy crawl blogs.oschina'.split(' '))
