# -*- coding: utf-8 -*-

# Define your item pipeline here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from pip import logger

from CuteScrapy.model.movies import Movies
from CuteScrapy.util.MysqlUtils import ORM
from CuteScrapy.model.blogs import Blogs


class CutescrapyPipeline(object):
    def __init__(self):
        self.orm = ORM()

    def process_item(self, item, spider):
        if spider.name == 'movies.mp4ba':
            movie = Movies()
            now = datetime.datetime.now()
            movie.id = item['id']
            movie.site = item['site']
            movie.type = item['type']
            movie.name = item['name']
            movie.full_name = item['full_name']
            movie.total = item['total']
            movie.page_url = item['page_url']
            movie.download_url = item['download_url']
            movie.img_url = item['img_url']
            movie.health = item['health']
            movie.stars = item['stars']
            movie.e_dloaded = item['e_dloaded']
            movie.director = item['director']
            movie.publish_time = item['publish_time']

            movie.date_update = now.strftime('%Y-%m-%d %H:%M:%S')
            try:
                self.orm.addData(movie)
            except Exception as e:
                logger.error(e)
            pass
        else:
            now = datetime.datetime.now()
            blog = Blogs()
            blog.site = item['site']
            blog.url = item['url']
            blog.title = item['title']
            blog.label = item['label']
            blog.brief = item['brief']
            blog.post_date = item['post_date']
            blog.blog = item['blog']
            blog.author = item['author']
            blog.pv = item['pv']
            blog.num_reviews = item['num_reviews']
            blog.diggnum = item['diggnum']
            blog.burynum = item['burynum']
            blog.date_update = now.strftime('%Y-%m-%d %H:%M:%S')
            # self.writeMetaFile(blog.title+','+blog.url+','+blog.label+','+blog.brief)

            try:
                self.orm.addData(blog)
            except Exception as e:
                logger.error(e)
