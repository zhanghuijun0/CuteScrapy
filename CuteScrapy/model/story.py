# coding:utf8
from CuteScrapy.util.MysqlUtils import ORM
from sqlalchemy import Column, String, FLOAT, INTEGER, ForeignKey, DateTime, BOOLEAN, TEXT, UniqueConstraint, Index, \
    TIMESTAMP
from datetime import datetime


Base = ORM.getBase()
orm = ORM()


class Story(Base):
    __tablename__ = 'story'

    id = Column(String(100), primary_key=True)
    site = Column(String(100))  # 站点
    title = Column(String(100))  # 小说名
    author = Column(String(100))  # 作者
    type = Column(String(100))  # 类型
    page_url = Column(TEXT)  # 链接
    last_sections = Column(TEXT)  # 最新章节
    update_date = Column(TIMESTAMP)
    date_update = Column(DateTime, default=datetime.now)
    date_create = Column(DateTime, default=datetime.now)


if __name__ == '__main__':
    orm = ORM()
    orm.initTable()
