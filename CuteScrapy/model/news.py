# coding:utf8
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func
from sqlalchemy.sql.elements import and_, or_
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime, BOOLEAN, TEXT, UniqueConstraint, Index, \
    TIMESTAMP, DATE
import datetime

from sqlalchemy.util import column_dict

from CuteScrapy.util.MysqlUtils import ORM

Base = ORM.getBase()
orm = ORM()


class News(Base):
    __tablename__ = 'news'
    id = Column(String(100), primary_key=True)
    site = Column(String(100))
    type = Column(String(100))
    title = Column(TEXT)
    keyword = Column(String(100))
    summary = Column(TEXT)
    content = Column(TEXT)
    positive = Column(FLOAT)
    negative = Column(FLOAT)
    page_url = Column(TEXT)
    status = Column(INTEGER)
    publish_time = Column(TIMESTAMP)  # 发布时间
    comment_time = Column(TIMESTAMP)  # 评论时间
    date_create = Column(DateTime, default=datetime.datetime.now)

    @classmethod
    def isExistById(cls, id):
        session = orm.getSession()
        if session.query(cls).filter(cls.id == id).first():
            tag = True
        else:
            tag = False
        session.close()
        return tag

    @classmethod
    def getDataByLastDay(cls, keyword, days=1):
        now = datetime.datetime.now()
        yesterday_now = now.strftime('%Y-%m-%d %H:%M:%S')
        day30_now = now - datetime.timedelta(days)
        session = orm.getSession()
        result = session.query(cls).filter(
            and_(News.comment_time.between(day30_now, yesterday_now),
                 News.keyword == keyword)).order_by(cls.comment_time.desc()).all()
        session.close()
        return result

    @classmethod
    def getKeyWords(cls):
        session = orm.getSession()
        result = session.query(cls.keyword).group_by(cls.keyword).all()
        session.close()
        return result

    @classmethod
    def getDataBySiteType(cls, site, _type):
        session = orm.getSession()
        result = session.query(cls).filter(cls.site == site, cls.type == _type).all()
        session.close()
        return result

    @classmethod
    def getAllData(cls):
        session = orm.getSession()
        result = session.query(cls).filter(cls.comment_time == None).all()
        session.close()
        return result


# class OpinionComment(Base):
#     __tablename__ = 'opinion_comment'
#     id = Column(String(100), primary_key=True)
#     o_id = Column(String(100), ForeignKey(News.id))
#     site = Column(String(100))
#     keyword = Column(String(100))
#     title = Column(String(200))
#     floor = Column(String(100))
#     comment = Column(TEXT)
#     positive = Column(FLOAT)
#     negative = Column(FLOAT)
#     url = Column(TEXT)
#     comment_time = Column(TIMESTAMP)  # 评论时间
#     date_create = Column(DateTime, default=datetime.datetime.now)
#
#     @classmethod
#     def isExistById(cls, id):
#         session = orm.getSession()
#         if session.query(cls).filter(cls.id == id).first():
#             tag = True
#         else:
#             tag = False
#         session.close()
#         return tag
#
#     @classmethod
#     def getReplyByOid(cls, o_id):
#         session = orm.getSession()
#         result = session.query(cls).filter(cls.o_id == o_id).all()
#         session.close()
#         return result
#
#     @classmethod
#     def getDataByLastDay(cls, keyword, days=1):
#         now = datetime.datetime.now()
#         yesterday_now = now.strftime('%Y-%m-%d %H:%M:%S')
#         day30_now = now - datetime.timedelta(days)
#         session = orm.getSession()
#         result = session.query(cls).filter(
#             and_(cls.comment_time.between(day30_now, yesterday_now), cls.keyword == keyword)).order_by(
#             cls.comment_time.desc()).all()
#         session.close()
#         return result
#
#     @classmethod
#     def getCommentsByOid(cls, o_id, days=1):
#         now = datetime.datetime.now()
#         yesterday_now = now.strftime('%Y-%m-%d %H:%M:%S')
#         day30_now = now - datetime.timedelta(days)
#         session = orm.getSession()
#         result = session.query(cls).filter(
#             and_(cls.comment_time.between(day30_now, yesterday_now), cls.o_id == o_id)).order_by(
#             cls.comment_time.desc()).all()
#         session.close()
#         return result


class NewsModel(Base):
    __tablename__ = 'news_model'
    id = Column(INTEGER, primary_key=True)
    keywords = Column(String(100))  # 关键字
    type = Column(String(100))  # 类型
    site = Column(String(100))  # 爬取站点
    sentiment = Column(BOOLEAN, default=False)  # 是否情感分析
    mail_group = Column(INTEGER)
    date_create = Column(DateTime, default=datetime.datetime.now)

    @classmethod
    def getKeyWords(cls):
        session = orm.getSession()
        result = session.query(cls).all()
        session.close()
        data = []
        for item in result:
            data.append(item.to_dict())
        return data

    def to_dict(cls):
        return {
            'id': cls.id,
            'keywords': cls.keywords,
            'type': cls.type,
            'site': cls.site,
            'sentiment': cls.sentiment
        }

    @classmethod
    def getEmailGroup(cls):
        session = orm.getSession()
        result = session.query(cls.mail_group).group_by(cls.mail_group).all()
        session.close()
        data = []
        for item in result:
            data.append(item.mail_group)
        return data

    @classmethod
    def getKeyWordsByGroup(cls, group):
        session = orm.getSession()
        result = session.query(cls).filter(cls.mail_group == group).all()
        session.close()
        data = []
        for item in result:
            data.append(item.to_dict())
        return data

    def column_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict


class NewsSubscibe(Base):
    __tablename__ = 'news_subscibe'
    mail = Column(String(100), primary_key=True)  # 邮件地址
    keywords = Column(String(100))  # 关键字
    date_create = Column(DateTime, default=datetime.datetime.now)

    @classmethod
    def getReceiverList(cls):
        session = orm.getSession()
        result = session.query(cls).all()
        session.close()
        return result


if __name__ == '__main__':
    orm = ORM()
    orm.initTable()
    # OpinionModel().getEmailGroup()
