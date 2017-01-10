# coding:utf8
# 导入:
from scrapy.utils import project
from sqlalchemy import Column, String, create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class ORM():
    baseCls = None

    def __init__(self):
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

    def addData(self, model):
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

class ORM2(object):
    '''
    orm = ORM()
    orm.commit(model) / orm.commit([modelA,modelB])
    '''
    baseCls = None
    _instance = {}

    def __new__(cls, *args, **kwargs):
        settings = project.get_project_settings()
        sql_uri = settings.get('SCRAPY_MYSQL_URL')
        if args:
            sql_uri = args[0]
        if sql_uri not in cls._instance:
            cls._instance[sql_uri] = object.__new__(cls)
            cls._instance[sql_uri]._engine = create_engine(sql_uri)
        return cls._instance[sql_uri]

    @classmethod
    def getBase(cls):
        if not ORM.baseCls:
            ORM.baseCls = declarative_base()
        return ORM.baseCls

    @classmethod
    def get_orm(cls, db_name):
        if db_name == 'scrapy':
            return ORM()
        if db_name == 'etl':
            settings = project.get_project_settings()  # get settings
            MYSQL_HOST = settings.get('ETL_MYSQL_HOST')
            MYSQL_PORT = settings.getint('ETL_MYSQL_PORT')
            MYSQL_USER = settings.get('ETL_MYSQL_USER')
            MYSQL_PASSWD = settings.get('ETL_MYSQL_PASSWD')
            MYSQL_DB = settings.get('ETL_MYSQL_DB')
            etl_orm = ORM('mysql+mysqlconnector://%s:%s@%s:%d/%s' % (
                MYSQL_USER, MYSQL_PASSWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB))
            return etl_orm
        if db_name == 'warehouse':
            settings = project.get_project_settings()  # get settings
            MYSQL_HOST = settings.get('WAREHOUSE_MYSQL_HOST')
            MYSQL_PORT = settings.getint('WAREHOUSE_MYSQL_PORT')
            MYSQL_USER = settings.get('WAREHOUSE_MYSQL_USER')
            MYSQL_PASSWD = settings.get('WAREHOUSE_MYSQL_PASSWD')
            MYSQL_DB = settings.get('WAREHOUSE_MYSQL_DB')
            warehouse_orm = ORM('mysql+mysqlconnector://%s:%s@%s:%d/%s' % (
                MYSQL_USER, MYSQL_PASSWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB))
            return warehouse_orm

    def _getEngine(self):
        # engine = create_engine(self.SCRAPY_MYSQL_HOST)
        # return engine
        return self._engine

    def getSession(self):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        return session

    @property
    def engine(self):
        return self._engine

    @property
    def session(self):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        return session

    def initTable(self):
        ORM.getBase().metadata.create_all(self.engine)

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

    def isExist(self, model, modelObjectId):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        flag = session.query(model.id).filter_by(id=modelObjectId).count() > 0
        session.close()
        return flag

    def find_one(self, model_class, filter_by):
        session = self.getSession()
        try:
            model = session.query(model_class).filter_by(**filter_by).first()
            return model
        except Exception, e:
            print e
            pass
        finally:
            session.close()

    def find_all(self, model_class, filter_by):
        session = self.getSession()
        try:
            for model in session.query(model_class).filter_by(**filter_by).all():
                yield model
        except Exception, e:
            print e
            pass
        finally:
            session.close()
