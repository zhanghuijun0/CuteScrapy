# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlogsItem(scrapy.Item):
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


class MovieItem(scrapy.Item):
    id = scrapy.Field()
    site = scrapy.Field()
    type = scrapy.Field()
    name = scrapy.Field()
    full_name = scrapy.Field()
    total = scrapy.Field()
    page_url = scrapy.Field()
    download_url = scrapy.Field()
    img_url = scrapy.Field()
    health = scrapy.Field()
    stars = scrapy.Field()
    e_dloaded = scrapy.Field()
    director = scrapy.Field()
    publish_time = scrapy.Field()


    date_update = scrapy.Field()
    date_create = scrapy.Field()