# coding:utf8
import hashlib
import json
import traceback
import re
from scrapy.cmdline import execute
from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider
from CuteScrapy.item.ModelItem import ModelItem
from CuteScrapy.model.wechat import WechatModel
from CuteScrapy.util.CommonParser import CommonParser

__author__ = 'HuijunZhang'

pattern = '<[^>]*>'


# 微信公众号抓取(新榜)
class WeixinArticleModelSplider(CrawlSpider):
    name = 'article.weixin.model'
    custom_settings = {
        'RETRY_TIMES': 50,
        'ITEM_PIPELINES': {
            'CuteScrapy.pipelines.MysqlORMPipeline': 300
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'CuteScrapy.middlewares.RandomProxyMiddleware': 800,
            'CuteScrapy.middlewares.UserAgentMiddleware': 600
        },
        'DOWNLOAD_TIMEOUT': 120,
        'CONCURRENT_REQUESTS': 5,
        'REACTOR_THREADPOOL_MAXSIZE': 10
    }

    def __init__(self, *args, **kwargs):
        super(WeixinArticleModelSplider, self).__init__(*args, **kwargs)
        self.commonParser = CommonParser()
        self.params = [
            'filter=&hasDeal=false&keyName=囧哥&order=NRI&nonce=02b470cba&xyz=fea918dd8f8c6ef11e86c133488307d0',
            'filter=&hasDeal=false&keyName=Android&order=NRI&nonce=3be259249&xyz=6791f97678b068f073d20b50dfd7f539',
            'filter=&hasDeal=false&keyName=Python&order=NRI&nonce=70445ca16&xyz=260e43ae615c94b2eaca971e3ce73703',
            'filter=&hasDeal=false&keyName=数据&order=NRI&nonce=9dd7a9958&xyz=fbd59bf9a2f3f9182a64fb692fd0235b',
            'filter=&hasDeal=false&keyName=开发&order=NRI&nonce=c5578b10b&xyz=b3d0e82ccc5661fd3263a602a69623d0',
            'filter=&hasDeal=false&keyName=admin10000_com&order=NRI&nonce=16fc1edb8&xyz=a14ec9997de44d523c0a32cbbf23da77',
            'filter=&hasDeal=false&keyName=admin10000_com&order=NRI&nonce=ee82c8939&xyz=f2c64b494328ab6d6f03fbad9595c439',
            'filter=&hasDeal=false&keyName=Google_Developers&order=NRI&nonce=3ad6a673e&xyz=d465a25f578dab82dcb69f8c66ead7cb',
            'filter=&hasDeal=false&keyName=Google_Developers&order=NRI&nonce=5937876ac&xyz=64647fbb63128bd5cbb264be60be540b',
            'filter=&hasDeal=false&keyName=开发者&order=NRI&nonce=5ef9f5d58&xyz=3bf9b02f655db2fd5bbeef90b3ac4e63',
            'filter=&hasDeal=false&keyName=河南科技学院&order=relation&nonce=41f213076&xyz=49025d05d71cac5e505dfe3e37fd238c',
            'filter=&hasDeal=false&keyName=核心商业机密&order=NRI&nonce=3cb397b76&xyz=a175e9ed375709c3e844a16fde9dbd01'
        ]

    def start_requests(self):
        for param in self.params:
            fromdata = self.commonParser.getDictFromString(param)
            yield FormRequest(
                "http://www.newrank.cn/xdnphb/data/weixinuser/searchWeixinDataByCondition",
                formdata=fromdata,
                meta={'type': 'list', 'fromdata': fromdata},
                dont_filter=True
            )

    def parse(self, response):
        if response.meta['type'] == 'list':
            for item in self.parse_list(response):
                yield item

    def parse_list(self, response):
        result = json.loads(response.body_as_unicode())
        if result.get('success'):
            for item in result.get('value').get('result'):
                try:
                    if item.get('account') is None:
                        self.logger.info(
                            '%s is not crawl!' % re.sub(pattern, '', item.get('name') or item.get('description')))
                        continue
                    wechatModel = WechatModel()
                    wechatModel.account = item.get('account')
                    wechatModel.name = re.sub(pattern, '', item.get('name'))
                    wechatModel.categories = item.get('type')
                    wechatModel.tags = re.sub(pattern, '', ','.join(item.get('tags'))) if item.get('tags') else None
                    wechatModel.description = re.sub(pattern, '', item.get('description'))
                    wechatModel.qrcode_img = item.get('codeImageUrl')
                    wechatModel.icon_img = item.get('headImageUrl')
                    wechatModel.xb_url = 'http://www.newrank.cn/public/info/detail.html?account=%s' % item.get(
                        'account')
                    yield ModelItem.getInstance(wechatModel)
                except Exception as e:
                    traceback.print_exc()


if __name__ == '__main__':
    execute('scrapy crawl article.weixin.model'.split(' '))
