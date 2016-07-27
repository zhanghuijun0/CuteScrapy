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
        blog.blog_type = item['blog_type']
        blog.article_url = item['article_url']
        blog.article_title = item['article_title']
        blog.brief = item['brief']
        blog.dateline = item['dateline']
        blog.blog_url = item['blog_url']
        blog.nick_name = item['nick_name']
        blog.label = item['label']
        blog.date_update = now.strftime('%Y-%m-%d %H:%M:%S')
        # logger.info(blog.article_url + ',' + blog.article_title+','+blog.dateline)
        try:
            self.orm.addData(blog)
        except Exception as e:
            print e