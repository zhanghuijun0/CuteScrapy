# coding:utf8
from sqlalchemy.orm import relationship, backref

from CuteScrapy.util.MysqlUtils import ORM
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime, BOOLEAN, TEXT, UniqueConstraint, Index, \
    TIMESTAMP
from datetime import datetime
from sqlalchemy import func

Base = ORM.getBase()
orm = ORM()


class Applet(Base):
    __tablename__ = 'applet'

    id = Column(String(100), primary_key=True)
    site = Column(String(100))  # 站点
    name = Column(String(100))  # 标题
    author = Column(String(100))  # 作者
    label = Column(String(100))  # 标签
    summary = Column(TEXT)  # 简介
    star = Column(INTEGER)  # 星级
    heart = Column(INTEGER)  # 喜欢
    share = Column(INTEGER)  # 分享
    page_url = Column(TEXT)  # 链接
    icon = Column(String(200))  # 图标
    qrcode = Column(TEXT)  # 小程序二维码
    pictures = Column(TEXT)  # 群应用截图
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

if __name__ == '__main__':
    orm = ORM()
    orm.initTable()
