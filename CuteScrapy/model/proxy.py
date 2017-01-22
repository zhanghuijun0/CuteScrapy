# coding:utf8
from CuteScrapy.util.CommonParser import CommonParser
from CuteScrapy.util.MysqlUtils import ORM
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime, BOOLEAN, TEXT, UniqueConstraint, Index, \
    TIMESTAMP
from datetime import datetime

__author__ = 'HuijunZhang'

Base = ORM.getBase()
orm = ORM()


class Proxy(Base):
    __tablename__ = 'proxy'
    id = Column(String(100), primary_key=True)
    site = Column(String(100))  # 站点
    ip = Column(String(100))  # ip
    port = Column(String(10))  # 端口
    type = Column(String(100))  # 类型:http,https,socks4/5
    site_conn_time = Column(String(100))  # 连接时间
    province = Column(String(100))
    city = Column(String(100))
    anonymity = Column(BOOLEAN)  # 高匿
    date_update = Column(DateTime, default=datetime.now)
    date_create = Column(DateTime, default=datetime.now)

    @classmethod
    def getProxyData(cls, _type='HTTP'):
        session = orm.getSession()
        result = session.query(cls).filter(cls.type == _type).all()
        session.close()
        return result

    @classmethod
    def delByid(cls, id):
        session = orm.getSession()
        proxy = Proxy()
        proxy.id = id
        result = session.query(cls).filter(cls.id == id).delete()
        session.commit()
        session.close()
        return result


if __name__ == '__main__':
    orm = ORM()
    # orm.initTable()
