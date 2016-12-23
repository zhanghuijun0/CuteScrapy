# coding:utf8
import requests
import json

import time

import logging

logger_dict = {

}

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
ch.setFormatter(formatter)


def getLogger(name='root', level='debug'):
    if name in logger_dict.keys():
        return logger_dict[name]
    else:
        logger = logging.getLogger(name)
        logger.propagate = False
        if level.lower() == 'debug':
            logger.setLevel(logging.DEBUG)
        if level.lower() == 'info':
            logger.setLevel(logging.INFO)
        if level.lower() == 'error':
            logger.setLevel(logging.ERROR)
        if not logger.handlers:
            logger.addHandler(ch)
        logger_dict[name] = logger
        return logger


__author__ = 'HuijunZhang'

requestUtil = requests
logging = getLogger('douding')


class DouDing():
    '''
    豆丁书房app签到
    '''

    def __init__(self):
        self.url = ''
        self.account = 'SseI6658lTF7a4LG-SWq3VXL-N3B2YjS'
        self.pwd = 'jX8VYeNPvrQWX-V6ludWqNC4Zlws9uqo'
        # 6, 10, 16, 20, 28, 51
        # self.award = {'_type':1,'award':6}
        # self.award = {'_type':2,'award':10}
        # self.award = {'_type':5,'award':16}
        # self.award = {'_type': 1, 'award': 20}
        # self.award = {'_type':2,'award':28}
        # self.award = {'_type': 10, 'award': 51}

    def get_keep_signin(self):
        '''
        签到界面
        :return:必须的参数
        '''
        data = {
            "value": '{"account":"%s","pwd":"%s","engine_id":"Android_BookStore","version":"7.00","type":"signinlist","device_info":{"model":"android","screen":"1080x1920"},"body":{"uid":"74057200"}}' % (
                self.account, self.pwd)
        }
        result = requestUtil.post('http://116.213.76.136/newboutiquebook.do', data=data)
        data = json.loads(result.text)
        if data.get('result') == '0000':
            param = data.get('body')
            logging.info('连续签到%s天,共签到%s天,总计获得%s豆点' % (
                param.get('keep_signin'), param.get('total_signin'), param.get('total_coin')))
            return param
        else:
            return None

    def do_qiandao(self, param):
        '''
        签到
        :param param:签到界面获取的参数
        :return:
        '''
        signin_day = param.get('today')
        keep_signin = param.get('keep_signin')
        data = {
            "value": '{"account":"%s","pwd":"%s","engine_id":"Android_BookStore","version":"7.00","type":"usersignin","device_info":{"model":"android","screen":"1080x1920"},"body":{"uid":"74057200","type":1,"signin_day":%s,"keep_signin":%s}}' % (
                self.account, self.pwd, signin_day, keep_signin)
        }
        result = requestUtil.post('http://116.213.76.136/newboutiquebook.do', data=data)
        data = json.loads(result.text)
        if data.get('result') == '0000':
            logging.info('签到成功')
        else:
            logging.error('签到失败')

    def get_lottery_list(self, param):
        '''
        抽奖界面
        :param param:签到界面获取的参数
        :return:待定
        '''
        _type = 1
        lottery_day = param.get('today')
        data = {
            "value": '{"account":"%s","pwd":"%s","engine_id":"Android_BookStore","version":"7.00","type":"lotterylist","device_info":{"model":"android","screen":"1080x1920"},"body":{"uid":"74057200","type":"%s","lottery_day":%s}}' % (
                self.account, self.pwd, _type, lottery_day)
        }
        result = requestUtil.post('http://116.213.76.136/newboutiquebook.do', data=data)  # 抽奖list
        data = json.loads(result.text)
        if data.get('result') == '1002':
            logging.warning(u'抽奖界面:%s' % data.get('body').get('reason'))
        elif data.get('result') == '0000':
            # TODO 查看 result
            lottery_number = data.get('body').get('lottery_number')
            lottery_result = data.get('body').get('lottery_result')
            logging.info('lottery_number:%s,lottery_result:%s' % (lottery_number, lottery_result))
            time.sleep(1)
            return data.get('body')
        else:
            logging.error('抽奖界面error:%s' % result.text)

    def do_choujiang(self, param2):
        '''
        抽奖
        :return:
        '''
        _type = 2
        award = param2.get('lottery_result')
        data = {
            "value": '{"account":"%s","pwd":"%s","engine_id":"Android_BookStore","version":"7.00","type":"userlottery","device_info":{"model":"android","screen":"1080x1920"},"body":{"uid":"74057200","type":"%s","award":%s}}' % (
                self.account, self.pwd, _type, award)
        }
        result = requestUtil.post('http://116.213.76.136/newboutiquebook.do', data=data)  # 抽奖list
        data = json.loads(result.text)
        if data.get('result') == '1002':
            logging.error(data.get('body').get('reason'))
        elif data.get('result') == '0000':
            logging.info(u'_type:%s,抽奖成功,获得%s豆点' % (_type, award))
        else:
            logging.error(u'抽奖失败')

    def run(self):
        '''
        主入口
        :return:
        '''
        result = self.get_keep_signin()
        if result:
            self.do_qiandao(result)
            param2 = self.get_lottery_list(result)
            if not param2:
                return
            while int(param2.get('lottery_result')) <= 20:
                param2 = self.get_lottery_list(result)
            self.do_choujiang(param2)
            logging.info(result)
        else:
            logging.error('获取签到列表失败,请重新登录')


if __name__ == '__main__':
    result = DouDing().run()
