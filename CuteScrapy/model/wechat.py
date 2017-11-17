# coding:utf8
from CuteScrapy.util.MysqlUtils import ORM
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime, BOOLEAN, TEXT, UniqueConstraint, Index, \
    TIMESTAMP
from datetime import datetime

Base = ORM.getBase()
orm = ORM()


class Article(Base):
    __tablename__ = 'article'

    id = Column(String(100), primary_key=True)
    site = Column(String(100))  # 站点
    publish_time = Column(TIMESTAMP)
    date_create = Column(DateTime, default=datetime.now)

    @classmethod
    def isExistById(cls, id):
        session = orm.getSession()
        if session.query(cls).filter(cls.id == id).first():
            tag = True
        else:
            tag = False
        session.close()
        return tag


class WechatModel(Base):
    __tablename__ = 'wechat_model'

    account = Column(String(100), primary_key=True)  # 微信号
    name = Column(String(100))  # 微信公众号
    categories = Column(String(100))  # 分类
    tags = Column(String(100))  # 标签
    description = Column(TEXT)
    qrcode_img = Column(TEXT)  # 二维码
    icon_img = Column(TEXT)  # 图标
    xb_url = Column(TEXT)
    is_check = Column(BOOLEAN, default=False)
    date_create = Column(DateTime, default=datetime.now)


if __name__ == '__main__':
    orm = ORM()
    orm.initTable()
