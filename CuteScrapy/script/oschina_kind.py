# coding:utf8
__author__ = 'zhanghj'
import requests
from lxml import etree
import json
import re


# 保存开源中国分类为json文件
class OsChinaHelper():
    def getkinds_oschina(self):
        text = u"<li><a href='/blog?type=428602' class='tag'>移动开发</a></li><li><a href='/blog?type=428612' class='tag'>前端开发</a></li><li><a href='/blog?type=428640' class='tag'>服务端开发/管理</a></li><li><a href='/blog?type=429511' class='tag'>游戏开发</a></li><li><a href='/blog?type=42860' class='tag'>编程语言</a></li><li><a href='/blog?type=428610' class='tag'>数据库</a></li><li><a href='/blog?type=428611' class='tag'>企业开发</a></li><li><a href='/blog?type=428647' class='tag'>图像/多媒体</a></li><li><a href='/blog?type=428613' class='tag'>系统运维</a></li><li><a href='/blog?type=428638' class='tag'>软件工程</a></li><li><a href='/blog?type=428639' class='tag'>云计算</a></li><li><a href='/blog?type=430884' class='tag'>开源硬件</a></li><li><a href='/blog?type=430381' class='tag'>其他类型</a></li>"
        tree = etree.HTML(text)
        for item in tree.xpath('//li'):
            title = item.xpath('a/text()')[0]
            id = re.findall('\d+', item.xpath('a/@href')[0])[0]
            json_text = json.dumps({'id': id, 'title': title})
            self.wirtefile('oschina_kinds.json', json_text + ',')

    def wirtefile(self, filename, text):
        with open('../resource/' + filename, 'a') as f:
            f.write(text.encode('utf8'))


if __name__ == '__main__':
    osChinaHelper = OsChinaHelper()
    # osChinaHelper.getkinds_oschina()