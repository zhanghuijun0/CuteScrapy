# coding:utf8
# 导入:
from sqlalchemy import Column, String, create_engine,MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class ORM():
    baseCls = None

    def __init__(self):
        # settings = project.get_project_settings()  # get settings
        self.SCRAPY_MYSQL_HOST = 'mysql+mysqlconnector://root:@localhost:3306/crawl'
        self.engine = self._getEngine()

    @classmethod
    def getBase(cls):
        if not ORM.baseCls:
            ORM.baseCls = declarative_base()
        return ORM.baseCls

    def _getEngine(self):
        engine = create_engine(self.SCRAPY_MYSQL_HOST)
        return engine

    def getSession(self):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        return session

    def initTable(self):
        ORM.baseCls.metadata.create_all(self.engine)

    def add(self, modelObjects):
        try:
            DBSession = sessionmaker(bind=self.engine)
            session = DBSession()
            if type(modelObjects) is list:
                session.add_all(modelObjects)
            else:
                session.merge(modelObjects)
            session.commit()
            session.close()
            return True
        except Exception, e:
            print e
            return False

    def addData(self,model):
        session = self.getSession()
        session.merge(model)
        try:
            # 提交即保存到数据库:
            session.commit()
        except Exception as e:
            print e
        finally:
            # 关闭session:
            session.close()


