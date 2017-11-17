# coding:utf8
import hashlib
import MySQLdb
import requests
import datetime
from lxml import etree
from Crypto.Cipher import AES, DES3
from binascii import b2a_hex, a2b_hex
from itsdangerous import base64_encode, base64_decode

requestUtil = requests
proxy = 'http://182.37.57.186:809'
key = 'qazxhouseqazxhou'


class Main():
    def __init__(self):
        self.__BLOCK_SIZE_16 = AES.block_size

    def crawl(self, key):
        result = requestUtil.post('http://qer.youpiezi.cn:1688/so/getSo', data={'soStr': key},
                                  proxies={'http': proxy}).json()
        if not result: return
        tuple_list = []
        for item in result:
            real_name = item.get('name')
            real_link = item.get('link')
            size = item.get('size')
            id = 'qer_%s' % (hashlib.md5(real_link).hexdigest())
            name = self.encryt(real_name.encode('utf8'))
            link = self.encryt(real_link.encode('utf8'))
            date_create = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            _tuple = (id, name, link, size, date_create, real_name, real_link,)
            tuple_list.append(_tuple)
        self.insert(tuple_list)

    def insert(self, tuple_list):
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='crawl',
        )
        cur = conn.cursor()
        # 一次插入多条记录
        sqli = "insert ignore into torrent values(%s,%s,%s,%s,%s,%s,%s)"
        count = cur.executemany(sqli, tuple_list)
        if count > 0:
            print('add %s data into torrent' % count)
        cur.close()
        conn.commit()
        conn.close()

    def run(self):
        for i in [u'hello']:
            self.crawl(i)

    # 58加密
    def encryt(self, str):
        cipher = AES.new(key, AES.MODE_ECB)
        x = self.__BLOCK_SIZE_16 - (len(str) % self.__BLOCK_SIZE_16)
        if x != 0:
            str = str + chr(x) * x
        msg = cipher.encrypt(str)
        msg = b2a_hex(msg).upper()
        return msg

    # 58解密
    def decrypt(self, str):
        cipher = AES.new(key, AES.MODE_ECB)
        plain_text = cipher.decrypt(a2b_hex(str))
        return plain_text.rstrip('\0').replace('', '')

    # 测试代理地址
    def get_ip_address(self):
        result = requestUtil.get('http://www.baidu.com/s?wd=ip', proxies={'http': proxy})
        tree = etree.HTML(result.text)
        li = tree.xpath('//img[@src="//www.baidu.com/aladdin/img/tools/ip.png"]/../following-sibling::*[1]//text()')
        return ''.join(li).strip()


if __name__ == '__main__':
    print Main().get_ip_address()
    result = Main().run()
