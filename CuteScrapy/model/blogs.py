# coding:utf8
from sqlalchemy.orm import relationship, backref

from CuteScrapy.util.MysqlUtils import ORM
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime, BOOLEAN, TEXT, UniqueConstraint, Index, \
    TIMESTAMP
from datetime import datetime
from sqlalchemy import func

Base = ORM.getBase()
orm = ORM()


# class Blogs(Base):
#     __tablename__ = 'blogs_list_test'
#     # __table_args__ = (UniqueConstraint('article_url','dateline', name='uidx_ids'),)
#     #
#     # id = Column(INTEGER, primary_key=True)
#     site = Column(String(100))  # 站点
#     url = Column(String(200), primary_key=True)  # 链接
#     title = Column(String(100))  # 标题
#     label = Column(String(100))  # 标签
#     brief = Column(TEXT)  # 简介
#     post_date = Column(String(100))  # 发表日期
#     blog = Column(String(100))  # 博客地址
#     author = Column(String(100))  # 用户昵称
#     pv = Column(INTEGER)  # 浏览量
#     num_reviews = Column(INTEGER)  # 评论数量
#     content = Column(TEXT)  # 内容
#     diggnum = Column(INTEGER)  # 推荐数量
#     burynum = Column(INTEGER)  # 踩的数量
#
#     publish_time = Column(TIMESTAMP)
#     date_create = Column(DateTime, default=datetime.now)
#     date_update = Column(DateTime, default=datetime.now)
#
#     @classmethod
#     def getAll(cls):
#         session = ORM().getSession()
#         blogs = session.query(cls).order_by(Blogs.date_create.desc()).all()[0:10]
#         session.close()
#         return blogs
#
#     @classmethod
#     def getBlobsBySite(cls, site, page=0, pagesize=50):
#         session = ORM().getSession()
#         blogs = session.query(cls).filter(Blogs.site == site).order_by(Blogs.date_create.desc()).all()[
#                 page * pagesize:page * pagesize + pagesize]
#         session.close()
#         return blogs
#
#     @classmethod
#     def getCountBySite(cls, site):
#         session = ORM().getSession()
#         blogs = session.query(func.count(cls.url).label('count')).filter(Blogs.site == site).first()
#         session.close()
#         return blogs.count
#
#     def to_dict(self):
#         return {
#             'site': self.site,
#             'url': self.url,
#             'title': self.title,
#             'label': self.label,
#             'brief': self.brief,
#             'post_date': self.post_date,
#             'blog': self.blog,
#             'author': self.author,
#             'pv': self.pv,
#             'num_reviews': self.num_reviews,
#             'diggnum': self.diggnum,
#             'burynum': self.burynum,
#             'content': self.content,
#             'date_create': self.date_create.strftime('%Y-%m-%d %H:%M:%S'),
#             'date_update': self.date_update.strftime('%Y-%m-%d %H:%M:%S')
#         }
#
#     @classmethod
#     def isExistsBlogsByid(cls, id):
#         session = ORM().getSession()
#         movies = session.query(cls).filter(Blogs.id == id).first()
#         session.close()
#         return movies

class Blogs(Base):
    __tablename__ = 'blogs_list'

    id = Column(String(100), primary_key=True)
    site = Column(String(100))  # 站点
    title = Column(String(100))  # 标题
    label = Column(String(100))  # 标签
    author = Column(String(100))  # 用户昵称
    summary = Column(TEXT)  # 简介
    content = Column(TEXT)  # 内容
    avatar = Column(String(200))  # 头像
    page_url = Column(TEXT)  # 链接
    blog_url = Column(String(100))  # 博客地址
    pv = Column(INTEGER)
    uv = Column(INTEGER)
    cv = Column(INTEGER)  # 评论数量
    positive = Column(INTEGER)  # 推荐
    negative = Column(INTEGER)  # 反对
    publish_time = Column(TIMESTAMP)
    date_create = Column(DateTime, default=datetime.now)
    date_update = Column(DateTime, default=datetime.now)

    @classmethod
    def isExistById(cls, id):
        session = orm.getSession()
        if session.query(cls).filter(cls.id == id).first():
            tag = True
        else:
            tag = False
        session.close()
        return tag

        # @classmethod
        # def getAll(cls):
        #     session = ORM().getSession()
        #     blogs = session.query(cls).order_by(Blogs.date_create.desc()).all()[0:10]
        #     session.close()
        #     return blogs
        #
        # @classmethod
        # def getBlobsBySite(cls, site, page=0, pagesize=50):
        #     session = ORM().getSession()
        #     blogs = session.query(cls).filter(Blogs.site == site).order_by(Blogs.date_create.desc()).all()[
        #             page * pagesize:page * pagesize + pagesize]
        #     session.close()
        #     return blogs
        #
        # @classmethod
        # def getCountBySite(cls, site):
        #     session = ORM().getSession()
        #     blogs = session.query(func.count(cls.url).label('count')).filter(Blogs.site == site).first()
        #     session.close()
        #     return blogs.count
        #
        # def to_dict(self):
        #     return {
        #         'site': self.site,
        #         'url': self.url,
        #         'title': self.title,
        #         'label': self.label,
        #         'brief': self.brief,
        #         'post_date': self.post_date,
        #         'blog': self.blog,
        #         'author': self.author,
        #         'pv': self.pv,
        #         'num_reviews': self.num_reviews,
        #         'diggnum': self.diggnum,
        #         'burynum': self.burynum,
        #         'content': self.content,
        #         'date_create': self.date_create.strftime('%Y-%m-%d %H:%M:%S'),
        #         'date_update': self.date_update.strftime('%Y-%m-%d %H:%M:%S')
        #     }
        #
        # @classmethod
        # def isExistsBlogsByid(cls, id):
        #     session = ORM().getSession()
        #     movies = session.query(cls).filter(Blogs.id == id).first()
        #     session.close()
        #     return movies


if __name__ == '__main__':
    orm = ORM()
    # Blogs().getBlobsBySite('csdn')
    # orm.initTable()
    # 创建新User对象:
    # new_user = CheShangTong(nick_name='zhj', user_id='12')
    # orm.addData(new_user)
