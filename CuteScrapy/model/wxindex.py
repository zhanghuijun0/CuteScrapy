# coding:utf8
import hashlib
from datetime import datetime
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.sql.elements import and_, or_
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime, BOOLEAN, TEXT, UniqueConstraint, Index, \
    TIMESTAMP, DATE

from CuteScrapy.util.MysqlUtils import ORM

Base = ORM.getBase()
orm = ORM()


# 微信指数
class WXIndex(Base):
    __tablename__ = 'wx_index'
    id = Column(String(100), primary_key=True)
    keyword = Column(String(100))
    date = Column(DATE)
    wx_index = Column(DOUBLE)
    date_update = Column(DateTime, default=datetime.now)
    date_create = Column(DateTime, default=datetime.now)

    @classmethod
    def isExistById(cls, id):
        session = orm.getSession()
        if session.query(cls).filter(cls.id == id).all():
            tag = True
        else:
            tag = False
        session.close()
        return tag

    @classmethod
    def isExistByKeyAndDate(cls, key, date):
        session = orm.getSession()
        if session.query(cls).filter(and_(cls.keyword == key, cls.date == date)).all():
            tag = True
        else:
            tag = False
        session.close()
        return tag


class WXIndexModel(Base):
    __tablename__ = 'wx_index_model'
    key = Column(String(100), primary_key=True)
    value = Column(String(100))
    date_create = Column(DateTime, default=datetime.now)

    @classmethod
    def getKeywordsList(cls):
        session = orm.getSession()
        result = session.query(cls).filter(cls.value == 'keywords').all()
        session.close()
        res = []
        for item in result:
            res.append(item.key)
        return res

    @classmethod
    def getCookies(cls):
        session = orm.getSession()
        result = session.query(cls).filter(cls.key == 'cookies').first()
        session.close()
        return result.value


if __name__ == '__main__':
    orm = ORM()
    orm.initTable()
