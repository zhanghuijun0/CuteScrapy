# coding:utf8
import datetime
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from CuteScrapy.item.ModelItem import ModelItem
from CuteScrapy.model.proxy import Proxy
from CuteScrapy.util.CommonParser import CommonParser

__author__ = 'HuijunZhang'

# 西刺代理
class ProxySplider(CrawlSpider):
    name = 'proxy.xici'
    custom_settings = {
        'RETRY_TIMES': 50,
        'ITEM_PIPELINES': {
            'CuteScrapy.pipelines.MysqlORMPipeline': 300,
            # 'CuteScrapy.pipelines.JsonWriterPipeline': 350,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'CuteScrapy.middlewares.RandomProxyMiddleware': 800,
            'CuteScrapy.middlewares.UserAgentMiddleware': 600
        },
        'DOWNLOAD_TIMEOUT': 120,
        'CONCURRENT_REQUESTS': 2,
        'REACTOR_THREADPOOL_MAXSIZE': 10
    }

    def __init__(self, *args, **kwargs):
        super(ProxySplider, self).__init__(*args, **kwargs)
        self.site = 'xici'
        self.commonParser = CommonParser()

    def start_requests(self):
        yield Request(
            'http://www.xicidaili.com/wt/',
            meta={'type': 'list', 'page_no': 1},
            dont_filter=True
        )

    def parse(self, response):
        if response.status == 200:
            if response.meta['type'] == 'list':
                for item in self.parse_list(response):
                    yield item

    def parse_list(self, response):
        self.logger.info('page no is:%s' % response.meta['page_no'])
        for item in response.xpath('//table[@id="ip_list"]/tr'):
            list = item.xpath('td').extract()
            if not list: continue
            ip = item.xpath('td[2]//text()').extract_first()
            port = item.xpath('td[3]//text()').extract_first()
            anonymity = True if item.xpath('td[5]//text()').extract_first() == u'高匿' else False
            type = item.xpath('td[6]//text()').extract_first()

            url = '%s:%s' % (ip, port)
            result = self.commonParser.check_proxy(type, url)
            if not result.get('status'):
                self.logger.info('ip:%s is expires.' % url)
                continue
            else:
                print result
            city_list = self.commonParser.parseLocationByIp(ip)

            proxy = Proxy()
            proxy.id = url
            proxy.site = self.site
            proxy.ip = ip
            proxy.port = port
            proxy.type = type
            proxy.province = city_list.get('province')
            proxy.city = city_list.get('city')
            proxy.anonymity = True if anonymity == u'高匿名' else False
            proxy.site_conn_time = result.get('time')
            proxy.date_update = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield ModelItem.getInstance(proxy)
        next_page = response.xpath('//a[@class="next_page"]/@href').extract_first()
        if next_page and response.meta['page_no'] < 100:
            yield Request(
                'http://www.xicidaili.com%s' % next_page,
                meta={'type': 'list', 'page_no': response.meta['page_no'] + 1},
                dont_filter=True
            )


if __name__ == '__main__':
    execute('scrapy crawl proxy.xici'.split(' '))
