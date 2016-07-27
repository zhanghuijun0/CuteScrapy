# -*- coding: utf-8 -*-

# Define your item pipeline here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from pip import logger

from CuteScrapy.util.MysqlUtils import ORM
from CuteScrapy.model.blogs import Blogs


class CutescrapyPipeline(object):
    def __init__(self):
        self.orm = ORM()

    def process_item(self, item, spider):
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