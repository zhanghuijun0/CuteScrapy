# coding:utf8
from sqlalchemy.orm import relationship, backref

from CuteScrapy.util.MysqlUtils import ORM
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime, BOOLEAN, TEXT, UniqueConstraint, Index, \
    TIMESTAMP
from datetime import datetime

Base = ORM.getBase()


class Blogs(Base):
    __tablename__ = 'blogs_list_test'
    # __table_args__ = (UniqueConstraint('article_url','dateline', name='uidx_ids'),)
    #
    # id = Column(INTEGER, primary_key=True)
    site = Column(String(100))  # 站点
    url = Column(String(200), primary_key=True)  # 链接
    title = Column(String(100))  # 标题
    label = Column(String(100))  # 标签
    brief = Column(TEXT)  # 简介
    post_date = Column(String(100))  # 发表日期
    blog = Column(String(100))  # 博客地址
    author = Column(String(100))  # 用户昵称
    pv = Column(INTEGER)  # 浏览量
    num_reviews = Column(INTEGER)  # 评论数量
    diggnum = Column(INTEGER)  # 推荐数量
    burynum = Column(INTEGER)  # 踩的数量

    date_create = Column(DateTime, default=datetime.now)
    date_update = Column(DateTime, default=datetime.now)

    @classmethod
    def getAll(cls):
        session = ORM().getSession()
        blogs = session.query(cls).order_by(Blogs.date_create.desc()).all()[0:10]
        session.close()
        return blogs

    @classmethod
    def getBlobsBySite(cls, site, page=0, pagesize=50):
        session = ORM().getSession()
        blogs = session.query(cls).filter(Blogs.site == site).order_by(Blogs.date_create.desc()).all()[
                page * pagesize:page * pagesize + pagesize]
        session.close()
        return blogs


if __name__ == '__main__':
    orm = ORM()
    Blogs().getBlobsBySite('csdn')
    # orm.initTable()
    # 创建新User对象:
    # new_user = CheShangTong(nick_name='zhj', user_id='12')
    # orm.addData(new_user)
