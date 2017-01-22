# coding:utf8
from sqlalchemy.orm import relationship, backref

from CuteScrapy.util.MysqlUtils import ORM
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime, BOOLEAN, TEXT, UniqueConstraint, Index, \
    TIMESTAMP
from datetime import datetime
from sqlalchemy import func

__author__ = 'HuijunZhang'

Base = ORM.getBase()
orm = ORM()


class Blogs(Base):
    __tablename__ = 'blogs'

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

    @classmethod
    def getBlogs(cls):
        session = orm.getSession()
        blogs = session.query(cls).order_by(cls.publish_time.desc()).all()[1:10]
        session.close()
        result = []
        for item in blogs:
            result.append(item.to_dict())
        return result

    def to_dict(self):
        return {
            'id': self.id,
            'site': self.site,
            'title': self.title,
            'label': self.label,
            'author': self.author,
            'summary': self.summary,
            'content': self.content,
            'avatar': self.avatar,
            'page_url': self.page_url,
            'blog_url': self.blog_url,
            'pv': self.pv,
            'uv': self.uv,
            'cv': self.cv,
            'positive': self.positive,
            'negative': self.negative,
            'publish_time': self.publish_time.strftime('%Y-%m-%d %H:%M:%S'),
            'date_create': self.date_create.strftime('%Y-%m-%d %H:%M:%S'),
            'date_update': self.date_update.strftime('%Y-%m-%d %H:%M:%S')
        }


if __name__ == '__main__':
    orm = ORM()
    # orm.initTable()
