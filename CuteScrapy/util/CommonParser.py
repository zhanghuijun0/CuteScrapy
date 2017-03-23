# coding:utf8
import zbar
from PIL import Image
import urllib
import cStringIO
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

    def getContentFromQrcode(self, url):
        result = []
        try:
            # 图片地址替换成你的qrcode图片地址
            # create a reader
            scanner = zbar.ImageScanner()
            # configure the reader
            scanner.parse_config('enable')
            # obtain image data
            imgfile = cStringIO.StringIO(urllib.urlopen(url).read())
            pil = Image.open(imgfile).convert('L')
            width, height = pil.size
            raw = pil.tobytes()
            # wrap image data
            image = zbar.Image(width, height, 'Y800', raw)
            # scan the image for barcodes
            scanner.scan(image)
            # extract results
            for symbol in image:
                # do something useful with results
                print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
                result.append(symbol.data)
            # clean up
            del (image)
        except Exception as e:
            logging.error('%s  get Qrcode failed!' % url)
        return result

    def replaceSpace(self, content):
        return '  '.join(self.trim(content).split())

    def getLatLonByCityName(self, cityName):
        url = "http://api.map.baidu.com/geocoder/v2/"
        data = {
            "address": cityName,
            "output": "json",
            "ak": "Ho67R16G4IhaBKwyKbHGd9yFbMRq54jq",
            "callback": ""
        }
        result = json.loads(requests.post(url, data=data).text)
        if result.get('status')==0:
            location = result.get('result').get('location')
            lat = location.get('lat')
            lng = location.get('lng')
            return lng,lat
        else:
            return None

if __name__ == '__main__':
    # print CommonParser().trim('dasNo')
    # print CommonParser().parseLocationByIp('61.152.81.193')
    # print CommonParser().parseLocationByIp('153.125.232.180')
    # print CommonParser().check_proxy('http', '124.88.67.32:80')
    # print CommonParser().getContentFromQrcode('https://ojib22q8q.qnssl.com/image/view/xcx_qrcode/4dc8a12d9a82c8c9c478637edabc06e2/300')
    # print CommonParser().getContentFromQrcode(
    #     'https://ojib22q8q.qnssl.com/image/view/xcx_qrcode/5c59efb121228be1c1668c409ea7b541/300')
    # print CommonParser().getContentFromQrcode(
    #     'http://media.ifanrusercontent.com/media/user_files/trochili/11/1c/111c1fef25db4e08704fbbd9a80ccc0234a158ef-e1470657bd8214aaeb029e32d9b755f60ac2b5f1.jpg')
    print CommonParser().getLatLonByCityName(u'东莞')