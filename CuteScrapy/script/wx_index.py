# coding:utf8
import hashlib
import json
import datetime
import traceback
import requests
import time

from CuteScrapy.model.wxindex import WXIndex, WXIndexModel
from CuteScrapy.util.MysqlUtils import ORM
from CuteScrapy.util.logger import getLogger

logging = getLogger('WXSearch')


class WXSearch():
    def __init__(self):
        self.orm = ORM()
        self.session = self.orm.getSession()
        self.wxindex = WXIndex()

    def run(self, keywords):
        logging.info(keywords)
        now = time.time()
        end_time = str('%.3f' % (now - 24 * 3600))
        start_time = str('%.3f' % (now - 90 * 24 * 3600))
        o = 1490609811174
        headers = {
            'Cookie': WXIndexModel.getCookies().encode('utf8'),
            'Referer': 'https://search.weixin.qq.com/cgi-bin/h5/wxindex/detail.html?q=%s&pass_ticket=zQE7LtY4Pl0uRAOeXONqdXkfeSp62IazVw4GAqC2u4nOO8pTXBfIL92x2f3h2BMe' % (
                keywords)
        }
        url = 'https://search.weixin.qq.com/cgi-bin/searchweb/getwxindex?query=%s&start_time=%s&end_time=%s&_=%s' % (
            keywords, start_time, end_time, o)
        response = requests.get(url, headers=headers)
        body = json.loads(response.text)
        if body.get('retcode') == 0:
            wxindex = body.get('data').get('wxindex')
            if wxindex != "":
                date_list = self.getDateList()
                wx_list = wxindex.split(',')
                try:
                    for item in zip(date_list, wx_list):
                        wxindex = WXIndex()
                        wxindex.keyword = keywords
                        wxindex.date = item[0]
                        wxindex.wx_index = float(item[1])
                        id = '%s%s%s' % (wxindex.keyword.decode('utf8'), wxindex.date.decode('utf8'), wxindex.wx_index)
                        wxindex.id = hashlib.md5(id.encode('gb2312')).hexdigest()
                        wxindex.date_update = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        if not self.wxindex.isExistById(wxindex.id):
                            self.orm.add(wxindex)
                except Exception as e:
                    traceback.print_exc()
                    logging.error(e)
            else:
                logging.error('%s:该词条未被收录' % keywords)
        else:
            logging.error(body.get('msg'))

    def getDateList(self):
        result = []
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=90)
        while start_date < end_date:
            result.append(start_date.strftime("%Y-%m-%d"))
            start_date += datetime.timedelta(1)
        return result


if __name__ == '__main__':
    search = WXSearch()
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    for item in WXIndexModel.getKeywordsList():
        item = item.encode('utf8')
        if not search.wxindex.isExistByKeyAndDate(item, yesterday):
            search.run(item)
        else:
            logging.info('%s is up to date!' % item)

            # ['佰仟融资租赁', '建元资本', '金磁融资租赁', '创富融资租赁', '优信', '车抵贷', '微贷网', '车闪贷', '58同城二手车', '微信', '乐天', '日本', '习近平','奥巴马', '特朗普', '小鲜肉', '颜值', '大数据', '朴槿惠', '鸡毛飞上天', '微信指数', '房价', '租房', '黑年', '京东', '淘宝', '每日优鲜', '支付宝', '天猫', '拼多多','余额宝', '美团', '饿了么', '阿里巴巴', '百度外卖', '大麦网', '大众点评', '菠萝蜜', '网易严选', '蘑菇街', '小红书', '日日顺', '苏宁易购', '美丽说', 'e代驾', 'eBay', '土巴兔', '返利网', '有棵树', '1号店', '蚂蚁金服', '小米', '华为', '马云', '马化腾', '张小龙']
