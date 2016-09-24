# coding:utf8
import re
import datetime
import traceback

from scrapy.cmdline import execute
from scrapy import Request
from scrapy.spiders import CrawlSpider
from scrapy.utils import project
from CuteScrapy.items import MovieItem
from CuteScrapy.model.movies import Movies
from CuteScrapy.util.DownloadHelper import Download


class DyxzwSplider(CrawlSpider):
    name = 'movies.dyxz5'

    def __init__(self, *args, **kwargs):
        super(DyxzwSplider, self).__init__(*args, **kwargs)
        self.site = 'dyxz5'
        self.base = 'http://www.dyxz5.com/'
        self.download = Download()
        self.settings = project.get_project_settings()  # get settings
        self.configPath = self.settings.get("DOWNLOAD_DIR")
        self.count = 0
        self.blogs = Movies()
        self.month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07',
                      'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    def start_requests(self):
        yield Request(
            self.base,
            meta={'type': 'list', 'pageNo': 1},
            dont_filter=True,
            headers={
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
        )

    def parse(self, response):
        if response.status == 200:
            if response.meta['type'] == 'list':
                for item in self.parse_list(response):
                    yield item
            elif response.meta['type'] == 'detail':
                for item in self.parse_detail(response):
                    yield item

    def parse_list(self, response):
        current_page_no = response.meta['pageNo']
        self.logger.info('========Crawl Page No:%s========' % (current_page_no))
        list = response.xpath('//*[@id="content"]/div[@class="main"]/ul/li')
        record_not_exist = True
        for item in list:
            try:
                movie = MovieItem()
                movie['site'] = self.site
                movie['page_url'] = item.xpath('div/h2/a/@href').extract_first()
                u_id = re.search('\/(\d+)', movie['page_url']).group(1)
                movie['id'] = '%s_%s' % (self.site, u_id)

                movie['full_name'] = item.xpath('div/h2/a/text()').extract_first().replace('\r\n', '').strip()
                try:
                    name = movie['full_name'].split(u'[BT下载]')[1].replace('[', '').split(u']')
                    movie['name'] = name[0]
                except:
                    # print movie['full_name']
                    movie['name'] = None

                movie['type'] = None
                # total_list = name[1].split('/')
                # if len(total_list) > 1:
                #     movie['total'] = total_list[1]
                movie['total'] = None

                movie['download_url'] = None
                movie['img_url'] = None
                movie['health'] = None
                movie['stars'] = None
                movie['director'] = None

                year = item.xpath('div/span[@class="date_y"]/text()').extract_first()
                month = item.xpath('div/span[@class="date_m"]/text()').extract_first()
                day = item.xpath('div/span[@class="date_d"]/text()').extract_first()
                month = self.month.get(month)
                movie['publish_time'] = datetime.datetime.strptime('%s-%s-%s' % (year, month, day), "%Y-%m-%d")

                info = item.xpath('div/div[@class="info"]/text()').extract()
                for pv in info:
                    if pv.find(u'阅读') > -1:
                        movie['e_dloaded'] = int(re.search('(\d+)', pv).group(1))
                        break
                if self.blogs.isExistsMoviesByid(movie['id']):
                    self.logger.info(
                        '*****************pageNo:%s,record exist! crawl total count:%s,title%s' % (
                            current_page_no, self.count, movie['full_name']))
                    record_not_exist = False
                    continue
                else:
                    self.count += 1
                    self.logger.info('----------Crawl No:%s,%s----------' % (self.count, movie['full_name']))
                    record_not_exist = True
                yield movie
            except Exception, e:
                traceback.print_exc()
                self.logger.error(str(e))
        next_page = response.xpath('//*[@id="pagenavi"]/a/@href').extract()[-1]
        next_page_no = int(response.xpath('//*[@id="pagenavi"]/a/@href').extract()[-1].split('/')[-1])
        if next_page_no > current_page_no and record_not_exist:
            yield Request(
                next_page,
                meta={'type': 'list', 'pageNo': next_page_no},
                dont_filter=True,
                headers={
                    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
            )
        else:
            self.logger.info('----------没有了,一共%s页----------' % (current_page_no))
        yield

    def parse_detail(self, response):
        create_date = response.xpath('//div[@class="article_info"]/text()').extract_first()
        create_date = re.search('(\d{4}-\d{2}-\d{2} \d{2}\:\d{2})', create_date).group(1)
        response.xpath('//div[@class="context"]/p/span/b/a/@href').extract_first()
        response.xpath('//div[@class="context"]/p/span/a/@href').extract_first()
        response.xpath('//div[@class="context"]/p/a/@href').extract_first()
        yield
        pass


if __name__ == '__main__':
    execute('scrapy crawl movies.dyxz5'.split(' '))
    # a = u'[2016][欧美][科幻][BT下载][伊利湖/怪异之湖 Lake Eerie][HD-MP4/3GB][中文字幕][1080P]'
    # a = u'[2016][欧美][喜剧][BT下载][爱情与友谊 Love & Friendship ][中文字幕][1080P]'
    # a = u'[欧美][喜剧][BD-1080P][BT下载]童子军手册之僵尸启示录/殭尸教战守则 1080p'
    # name = a.split(u'[BT下载]')[1].replace('[','').split(u']')
    # print name[0]
    # print name[1].split('/')[1]
