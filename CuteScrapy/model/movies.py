# coding:utf8
from sqlalchemy.orm import relationship, backref

from CuteScrapy.util.MysqlUtils import ORM
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime, BOOLEAN, TEXT, UniqueConstraint, Index, \
    TIMESTAMP
from datetime import datetime

Base = ORM.getBase()


class Movies(Base):
    __tablename__ = 'movies_list'
    # __table_args__ = (UniqueConstraint('article_url','dateline', name='uidx_ids'),)
    #
    id = Column(String(100), primary_key=True)
    site = Column(String(100))  # 站点
    type = Column(String(100))  # 分类
    name = Column(String(100))  # 名称
    full_name = Column(String(250))  # 全称
    total = Column(String(100))  # 大小
    page_url = Column(String(200))  # 页面url
    download_url = Column(String(200))  # 下载url
    img_url = Column(String(200))  # 图片url
    health = Column(String(100))  # 健康度
    stars = Column(String(100))  # 星级
    e_dloaded = Column(INTEGER)  # 下载量
    director = Column(String(200))  # 导演
    publish_time = Column(DateTime)  # 发布时间

    date_create = Column(DateTime, default=datetime.now)
    date_update = Column(DateTime, default=datetime.now)

    @classmethod
    def isExistsMoviesByid(cls, id):
        session = ORM().getSession()
        movies = session.query(cls).filter(Movies.id == id).first()
        session.close()
        return movies

if __name__ == '__main__':
    orm = ORM()
    orm.initTable()
