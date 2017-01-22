# coding:utf8
import json
import time
import requests
from CuteScrapy.util.logger import getLogger

__author__ = 'HuijunZhang'

ak = '05Unerzh8DGNMf78det8fZB2cPSQLVv3'  # 百度前端ak
logging = getLogger('commonparser')


class CommonParser():
    def __init__(self):
        pass

    def trim(self, string):
        if not string:
            return string
        string = string.replace(u'\r', u'').replace(u'\n', u'').replace(u'\t', u'')
        return string.strip()

    def parseLocationByIp(self, ip):
        '''
        http://lbsyun.baidu.com/index.php?title=webapi/ip-api
        :param ip:
        :return:
        '''
        response = requests.get('http://api.map.baidu.com/location/ip?ip=%s&ak=%s' % (ip, ak))
        result = {}
        if response.status_code == 200:
            body = json.loads(response.text)
            if body.get('status') == 0:
                city = body.get('content').get('address_detail').get('city')
                province = body.get('content').get('address_detail').get('province')
                result = {
                    'ip': ip,
                    'city': city,
                    'province': province
                }
            else:
                logging.error('get city error:%s' % body.get('message'))
        return result

    # Check proxy
    def check_proxy(self, type, ip):
        proxy = {'http': 'http://' + ip}
        timeout = 10
        result = {}
        try:
            time_start = time.time()
            response = requests.get('http://lwons.com/wx', proxies=proxy, timeout=timeout)
            time_end = time.time()
            if response.text == 'default':
                result = {
                    'ip': ip,
                    'status': True,
                    'time': round(time_end - time_start, 3)
                }
                print 'ip:%s,time:%s' % (ip, round(time_end - time_start, 3))
            else:
                result = {
                    'ip': ip,
                    'status': False,
                    'time': None
                }
        except Exception as e:
            result = {
                'ip': ip,
                'status': False,
                'time': None
            }
        return result


if __name__ == '__main__':
    # print CommonParser().trim('dasNo')
    # print CommonParser().parseLocationByIp('61.152.81.193')
    # print CommonParser().parseLocationByIp('153.125.232.180')
    print CommonParser().check_proxy('http', '124.88.67.32:80')
