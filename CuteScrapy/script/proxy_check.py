# coding:utf8
import time

from CuteScrapy.model.proxy import Proxy
from CuteScrapy.util.CommonParser import CommonParser
from CuteScrapy.util.logger import getLogger

__author__ = 'HuijunZhang'

logging = getLogger('ProxyCheck')


# 检测代理是否失效,并删除失效代理
class ProxyCheck():
    def __init__(self):
        self.proxy = Proxy()
        self.commonParser = CommonParser()

    def run(self):
        for item in self.proxy.getProxyData():
            result = CommonParser().check_proxy(item.type, item.id)
            if not result.get('status'):
                status = self.proxy.delByid(item.id)
                if not status:
                    logging.error('id:%s,delete failed' % item.id)
                else:
                    logging.info('id:%s is expires.' % item.id)
            time.sleep(5)


if __name__ == '__main__':
    count = 1
    while count < 10000:
        logging.info('----------count:%s----------' % count)
        ProxyCheck().run()
        count += 1
