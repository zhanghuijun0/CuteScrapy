# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CutescrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    blog_type = scrapy.Field()
    article_url = scrapy.Field()
    article_title = scrapy.Field()
    brief = scrapy.Field()
    dateline = scrapy.Field()
    blog_url = scrapy.Field()
    nick_name = scrapy.Field()
    label = scrapy.Field()