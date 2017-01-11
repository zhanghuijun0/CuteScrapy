# -*- coding: utf-8 -*-

# Define your item pipeline here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json

from pip import logger
import logging

from scrapy.utils import project
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from CuteScrapy.model.movies import Movies
from CuteScrapy.util.MysqlUtils import ORM
from CuteScrapy.model.blogs import Blogs


class CutescrapyPipeline(object):
    def __init__(self):
        self.orm = ORM()

    def process_item(self, item, spider):
        logging.info('default pipline,table name:%s' % spider.name)
        if type(item['model']) is list:
            for object in item['model']:
                for className in object.__dict__:
                    print '%s,:%s' % (className, object.__dict__[className])
                    pass
        else:
            object = item['model']
            for className in object.__dict__:
                print '%s,:%s' % (className, object.__dict__[className])
                pass
                # if spider.name == 'movies.mp4ba' or spider.name == 'movies.dyxz5':
                #     movie = Movies()
                #     now = datetime.datetime.now()
                #     movie.id = item['id']
                #     movie.site = item['site']
                #     movie.type = item['type']
                #     movie.name = item['name']
                #     movie.full_name = item['full_name']
                #     movie.total = item['total']
                #     movie.page_url = item['page_url']
                #     movie.download_url = item['download_url']
                #     movie.img_url = item['img_url']
                #     movie.health = item['health']
                #     movie.stars = item['stars']
                #     movie.e_dloaded = item['e_dloaded']
                #     movie.director = item['director']
                #     movie.publish_time = item['publish_time']
                #
                #     movie.date_update = now.strftime('%Y-%m-%d %H:%M:%S')
                #     try:
                #         self.orm.addData(movie)
                #     except Exception as e:
                #         logger.error(e)
                #     pass
                # else:
                #     now = datetime.datetime.now()
                #     blog = Blogs()
                #     blog.site = item['site']
                #     blog.url = item['url']
                #     blog.title = item['title']
                #     blog.label = item['label']
                #     blog.brief = item['brief']
                #     blog.post_date = item['post_date']
                #     blog.blog = item['blog']
                #     blog.author = item['author']
                #     blog.pv = item['pv']
                #     blog.num_reviews = item['num_reviews']
                #     blog.diggnum = item['diggnum']
                #     blog.burynum = item['burynum']
                #     blog.date_update = now.strftime('%Y-%m-%d %H:%M:%S')
                #     # self.writeMetaFile(blog.title+','+blog.url+','+blog.label+','+blog.brief)
                #
                #     try:
                #         self.orm.addData(blog)
                #     except Exception as e:
                #         logger.error(e)


class MysqlORMPipeline():
    def __init__(self):
        settings = project.get_project_settings()  # get settings
        SCRAPY_MYSQL_HOST = settings.get('SCRAPY_MYSQL_URL')
        self.engine = create_engine(SCRAPY_MYSQL_HOST)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def add(self, modelObjects):
        try:
            if type(modelObjects) is list:
                self.session.add_all(modelObjects)
            else:
                self.session.merge(modelObjects)
            self.session.commit()
            return True
        except Exception, e:
            print e
            return False

    def process_item(self, item, spider):
        kwargs = {}
        if type(item['model']) is list:
            for object in item['model']:
                if hasattr(object, 'beforeAdd'):
                    getattr(object, 'beforeAdd')(kwargs)
                if hasattr(object, 'date_update'):
                    setattr(object, 'date_update', datetime.datetime.now())
                flag = self.add(object)
                if hasattr(object, 'id') and getattr(object, 'id'):
                    logging.info('pipline : mysql %s : [%s : %s]' % (
                        'insert' if flag else 'update', object.__class__.__name__, str(getattr(object, 'id'))))
                else:
                    logging.info(
                        'pipline : mysql %s : %s' % ('insert' if flag else 'update', object.__class__.__name__))
                kwargs.update({object.__class__.__name__: object})
                if hasattr(object, 'afterInsert'):
                    getattr(object, 'afterInsert')(object, kwargs)
        else:
            object = item['model']
            if hasattr(object, 'beforeAdd'):
                getattr(object, 'beforeAdd')(kwargs)
            if hasattr(object, 'date_update'):
                setattr(object, 'date_update', datetime.datetime.now())
            flag = self.add(object)
            if hasattr(object, 'id') and getattr(object, 'id'):
                logging.info('pipline : mysql %s : [%s : %s]' % (
                    'insert' if flag else 'update', object.__class__.__name__, str(getattr(object, 'id'))))
            else:
                logging.info(
                    'pipline : mysql %s : %s' % ('insert' if flag else 'update', object.__class__.__name__))
            if hasattr(object, 'afterInsert'):
                getattr(object, 'afterInsert')(object, kwargs)
        return item

    def close_spider(self, spider):
        self.session.close()
        self.engine.dispose()


class JsonWriterPipeline():
    def __init__(self):
        self.file = open('items.json', 'wb')

    def process_item(self, item, spider):
        if type(item['model']) is list:
            for object in item['model']:
                object = object.__dict__
                object.pop('_sa_instance_state')
                line = json.dumps(object) + ',\n'
                self.file.write(line)
        else:
            object = item['model'].__dict__
            object.pop('_sa_instance_state')
            line = json.dumps(object) + ',\n'
            self.file.write(line)
