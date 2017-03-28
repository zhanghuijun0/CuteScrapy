# coding:utf8
import traceback

import MySQLdb
import time

import datetime

from CuteScrapy.util.CommonParser import CommonParser
from CuteScrapy.util.logger import getLogger

__author__ = 'zhanghj'
from CuteScrapy.resource.ResourceHelper import ResourceHelper
import requests
from lxml import etree
import json
import re

logging = getLogger('UpdateCityToLat')


# 城市转化为json
class UpdateCityToLat():
    def __init__(self):
        self.commonParser = CommonParser()
        self.my_conn = MySQLdb.connect(host='127.0.0.1',
                                       port=3306,
                                       user='root',
                                       passwd='',
                                       db='scrapy',
                                       charset="utf8")

    def run(self):

        pass

    def getData(self):
        result = None
        try:
            sql_str = 'select * from city_loca where lat is null;'
            cur = self.my_conn.cursor()
            count = cur.execute(sql_str)
            result = cur.fetchone()
            for item in cur.fetchmany(cur.execute(sql_str)):
                city_code = item[0]
                city = item[1]
                location = self.commonParser.getLatLonByCityName(city)
                if not location:continue
                lng = location[0]
                lat = location[1]
                # self.insertLocation(lng, lat, str(city_code))
                # self.insertLocation(lng, lat, str(city_code))
                print city, location
                time.sleep(0.5)
        except Exception, e:
            traceback.print_exc()
            logging.error(e)
        finally:
            cur.close()
        return count

    # def getLatLonByCityName(self, cityName):
    #     requests.post()
    #     pass

    def insertLocation(self, lng, lat, id):
        date_update = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "update city_loca set lng = '%s',lat = '%s',date_update = '%s' where id = '%s';" % (
            lng, lat, date_update, id)
        cur = self.my_conn.cursor()
        count = cur.execute(sql)
        self.my_conn.commit()
        print count


if __name__ == '__main__':
    updateCityToLat = UpdateCityToLat()
    data = updateCityToLat.getData()
    # data = updateCityToLat.insertLocation("123321",'00002')
    print data
