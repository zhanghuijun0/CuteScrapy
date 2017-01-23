# coding:utf8
import requests
import json

import time

import logging

from flask import jsonify

from CuteScrapy.item.ModelItem import ModelItem
from CuteScrapy.model.news import NewsModel
from CuteScrapy.util.MysqlUtils import ORM

orm = ORM()
session = orm.getSession()


class SubmitJson2mysql():
    def __init__(self):
        self.json = [{
            'id': 2,
            'keywords': u'禁言',
            'type': None,
            'site': 'weixin',
            'sentiment': False,
            'mail_group': 0
        }, {
            'id': 1,
            'keywords': u'余额宝1',
            'type': None,
            'site': 'weixin',
            'sentiment': False,
            'mail_group': 0
        }]
        self.json1 = '[{"mail_group": 0, "sentiment": false, "site": "weixin", "keywords": "金岩财富", "type": null, "id": 2}, {"mail_group": 0, "sentiment": false, "site": "weixin", "keywords": "余额宝", "type": null, "id": 1}]'

    def insertjson2mysql(self, model_object, json_object):
        '''
        将json字符串或对象插入到model_object相关的mysql
        :param model_object:json字符串或对象
        :param json_object:数据库model对象
        :return:
        self.json = [{
            'id': 2,
            'keywords': u'禁言',
            'type': None,
            'site': 'weixin',
            'sentiment': False,
            'mail_group': 0
        }, {
            'id': 1,
            'keywords': u'余额宝1',
            'type': None,
            'site': 'weixin',
            'sentiment': False,
            'mail_group': 0
        }]
        '''
        if type(json_object) is str:
            json_object = json.loads(json_object)
        if type(json_object) is list:
            for js in json_object:
                for key in js:
                    setattr(model_object, key, js[key])
                orm.add(model_object)
        else:
            for key in json_object:
                setattr(model_object, key, json_object[key])
            orm.add(model_object)

    def selectmysql2json(self, model_object):
        '''
        查找model_object(这个方法没太大用处,由于存在datetime类型,所以不能直接json.dumps)
        :param model_object:
        :return:
        '''
        list = []
        result = session.query(model_object).all()
        for item in result:
            list.append(item.column_dict())
        return list


if __name__ == '__main__':
    model = NewsModel()
