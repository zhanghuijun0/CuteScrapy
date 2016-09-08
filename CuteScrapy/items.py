# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CutescrapyItem(scrapy.Item):
    # define the fields for your item here like:
    site = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    label = scrapy.Field()
    brief = scrapy.Field()
    post_date = scrapy.Field()
    blog = scrapy.Field()
    author = scrapy.Field()
    pv = scrapy.Field()
    num_reviews = scrapy.Field()
    diggnum = scrapy.Field()
    burynum = scrapy.Field()
    date_update = scrapy.Field()
    date_create = scrapy.Field()
