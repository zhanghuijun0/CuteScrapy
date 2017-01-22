# coding:utf8
import re
import datetime
from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.utils import project
from CuteScrapy.items import MovieItem
from CuteScrapy.model.movies import Movies
from CuteScrapy.util.DownloadHelper import Download


class MovieSplider(CrawlSpider):
    name = 'movies.mp4ba'

    def __init__(self, *args, **kwargs):
        super(MovieSplider, self).__init__(*args, **kwargs)
        self.site = 'mp4ba'
        self.base = 'http://www.mp4ba.net/'
        self.download = Download()
        self.settings = project.get_project_settings()  # get settings
        self.configPath = self.settings.get("DOWNLOAD_DIR")
        self.count = 0
        self.blogs = Movies()

    def start_requests(self):
        yield Request(
            "http://www.mp4ba.net",
            meta={'type': 'home'},
            dont_filter=True,
            headers={
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
        )

    def parse(self, response):
        if response.status == 200:
            if response.meta['type'] == 'home':
                for item in self.parse_home(response):
                    yield item
            elif response.meta['type'] == 'list':
                for item in self.parse_list(response):
                    yield item
            elif response.meta['type'] == 'detail':
                for item in self.parse_detail(response):
                    yield item

    def parse_home(self, response):
        list = response.xpath('//*[@class="nav"]/ul/li')
        for item in list:
            kinds = item.xpath('a/text()').extract_first()
            url = item.xpath('a/@href').extract_first()
            if kinds == u'首页':
                continue
            path = u"%s%s/%s" % (self.configPath, self.site, kinds)
            # os.makedirs(path)
            yield Request(
                "http://www.mp4ba.com/%s" % url,
                meta={'type': 'list', 'pageNo': 1, 'download_path': path},
                dont_filter=True,
                headers={
                    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
            )

    def parse_list(self, response):
        pageNo = response.meta['pageNo']
        list = response.xpath('//*[@id="data_list"]/tr')
        if len(list) == 1 and response.xpath('//*[@id="data_list"]/tr/td/text()').extract_first() == u'没有可显示资源':
            self.logger.info('---%s,%s---' % (response.url, u'没有数据'))
            return
        self.logger.info('---pageNo:%s,%s---' % (pageNo, response.url))
        record_not_exist = True
        for item in list:
            # record_not_exist = True
            if len(item.xpath('td')) == 1:
                continue
            movie = MovieItem()
            movie['site'] = self.site
            movie['type'] = item.xpath('td[2]/a/text()').extract_first()
            movie['full_name'] = item.xpath('td[3]/a/text()').extract_first().replace('\r', '').replace('\n',
                                                                                                        '').strip()
            movie['name'] = movie['full_name'].split('.')[0]
            movie['total'] = item.xpath('td[4]/text()').extract_first()
            movie['page_url'] = self.base + item.xpath('td[3]/a/@href').extract_first()
            movie['id'] = '%s_%s' % (self.site, re.search('\?hash=(\w+)', movie['page_url']).group(1))

            if item.xpath('td[8]/a/text()').extract_first() != u'高清MP4吧':
                print item.xpath('td[8]/a/text()').extract_first()
            if self.blogs.isExistsMoviesByid(movie['id']):
                # self.logger.info(
                #     '*****************type:%s,pageNo:%s,record exist! crawl total count:%s,title%s*****************' % (
                #         movie['type'], pageNo, self.count, movie['full_name']))
                record_not_exist = False
                continue
            else:
                self.logger.info('------lastest file,type:%s,title%s-------' % (movie['type'], movie['full_name']))
                yield Request(
                    movie['page_url'],
                    meta={'type': 'detail', 'movie': movie, 'download_path': response.meta['download_path']},
                    dont_filter=True,
                    headers={
                        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
                )
        next_page = response.xpath('//*[@class="pages clear"]/a[@class="nextprev"]/@href').extract()
        if next_page and record_not_exist:
            next_page_no = int(re.search('page=(\d+)', next_page[-1]).group(1))
            if next_page_no > pageNo:
                yield Request(
                    "http://www.mp4ba.com/%s" % next_page[-1],
                    meta={'type': 'list', 'pageNo': next_page_no, 'download_path': response.meta['download_path']},
                    dont_filter=True,
                    headers={
                        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
                )

    def parse_detail(self, response):
        path = response.meta['download_path']
        movie = response.meta['movie']
        datestr = response.xpath('//*[@class="basic_info"]/p[4]/text()').extract_first()
        publish_time_str = re.search('(\d{4}\/\d{2}\/\d{2} \d{2}\:\d{2}\:\d{2})', datestr).group(1)
        movie['publish_time'] = datetime.datetime.strptime(publish_time_str, "%Y/%m/%d %H:%M:%S")
        movie['health'] = re.search('(\d+)',
                                    response.xpath('//*[@class="basic_info"]/p[7]/img/@src').extract_first()).group(1)
        movie['download_url'] = self.base + response.xpath('//*[@class="basic_info"]/p[8]/a/@href').extract_first()
        movie['img_url'] = response.xpath('//*[@class="intro"]/img[1]/@src').extract_first() or response.xpath(
            '//*[@class="intro"]/p/img[1]/@src').extract_first()
        movie['stars'] = None
        movie['e_dloaded'] = None
        movie['director'] = None
        yield movie
        save = '%s/%s.torrent' % (path, movie['full_name'])
        self.count += 1
        self.logger.info('********Crawl No:%s********' % (self.count))
        self.download.download(movie['download_url'], save)


if __name__ == '__main__':
    execute('scrapy crawl movies.mp4ba'.split(' '))
