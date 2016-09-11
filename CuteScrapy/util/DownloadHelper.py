# coding:utf8
import urllib
import urllib2
import requests
import time
import logging
from CuteScrapy.util.logger import getLogger
logging = getLogger('DownloadHelper')

# Python开发中时长遇到要下载文件的情况，最常用的方法就是通过Http利用urllib或者urllib2模块。
# 当然你也可以利用ftplib从ftp站点下载文件。此外Python还提供了另外一种方法requests。
# 下面来看看三种方法是如何来下载zip文件的：

class Download():
    def __init__(self):
        self.path = u'/Users/huijunzhang/百度云同步盘/zhj-mac/download/'
        # self.path = '\/Users\/huijunzhang'

    def download2(self, url, name):
        start = time.time()
        urllib.urlretrieve(url, self.path + name)
        end = time.time()
        logging.info('[%s]download  spend %s seconds' % (name, end - start))
        # print 'download [%s] spend %s seconds' % (name, end - start)

    def download1(self, url, name):
        start = time.time()
        f = urllib2.urlopen(url)
        data = f.read()
        with open(self.path + name, "wb") as code:
            code.write(data)
        end = time.time()
        logging.info('[%s]download spend %s seconds' % (name, end - start))

    def download(self, url, name):
        start = time.time()
        r = requests.get(url)
        with open(self.path + name, "wb") as code:
            code.write(r.content)
        end = time.time()
        logging.info('[%s]download spend %s seconds' % (name, end - start))


if __name__ == '__main__':
    # url = 'https://media.readthedocs.org/htmlzip/requests-docs-cn/latest/requests-docs-cn.zip'
    # name = u"requests-docs-cn.zip"
    # Download().download2(url, name)
    pass
