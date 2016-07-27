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

    # id = Column(INTEGER, primary_key=True)
    blog_type = Column(String(100))
    article_url = Column(String(100), primary_key=True)
    article_title = Column(String(100))
    brief = Column(TEXT)
    dateline = Column(String(100))
    blog_url = Column(String(100))
    nick_name = Column(String(100))
    label = Column(String(100))

    date_create = Column(DateTime, default=datetime.now)
    date_update = Column(DateTime, default=datetime.now)


if __name__ == '__main__':
    orm = ORM()
    orm.initTable()
    # 创建新User对象:
    # new_user = CheShangTong(nick_name='zhj', user_id='12')
    # orm.addData(new_user)

# ssh -N -p 22 -g zhanghuijun@jhost -L 3308:rdsn5s5x6z2h17xvaai5.mysql.rds.aliyuncs.com:3306