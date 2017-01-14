# coding:utf8
import datetime

import re

__author__ = 'HuijunZhang'


def parseDateString(dateStr):
    if not dateStr:
        return None
    else:
        dateStr = dateStr.strip()
    now = datetime.datetime.now()
    if re.search('\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}', dateStr):
        time = re.search('(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})', dateStr).group(1)
    elif re.search('\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}', dateStr):
        time = re.search('(\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2})', dateStr).group(1)
    elif re.search(u"(\d+)天前", dateStr):
        day_before = int(re.search(u"(\d+)天前", dateStr).group(1))
        day_before_n = (now - datetime.timedelta(days=day_before)).strftime('%Y-%m-%d')
        time = re.sub(u"(\d+)天前", day_before_n, dateStr)
    elif re.search(u"(\d+)小时前", dateStr):
        hour_before = int(re.search(u"(\d+)小时前", dateStr).group(1))
        time = (now - datetime.timedelta(hours=hour_before)).strftime('%Y-%m-%d %H:%M:%S')
    elif re.search(u"(\d+)分钟前", dateStr):
        minute_before = int(re.search(u"(\d+)分钟前", dateStr).group(1))
        time = (now - datetime.timedelta(minutes=minute_before)).strftime('%Y-%m-%d %H:%M:%S')
    elif re.search(u"昨天", dateStr):
        yesterday = (now - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        time = re.sub(u"昨天", yesterday, dateStr)
    elif re.search(u"前天", dateStr):
        day_before_yesterday = (now - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        time = re.sub(u"前天", day_before_yesterday, dateStr)
    else:
        time = dateStr
    return time

def timestamp2datetime(timestamp, convert_to_local=True):
    ''' Converts UNIX timestamp to a datetime object. '''
    if isinstance(timestamp, (int, long, float)):
        dt = datetime.datetime.utcfromtimestamp(timestamp)
        if convert_to_local:  # 是否转化为本地时间
            dt = dt + datetime.timedelta(hours=8)  # 中国默认时区
        return dt
    return timestamp

if __name__ == '__main__':
    print parseDateString(u'发布于 2017-01-10 18:10')
    print parseDateString(u'昨天 18:20')
    print parseDateString(u'3小时前')
    print parseDateString(u'前天 14:30')
    print parseDateString(u'6天前 10:27')
    print parseDateString(u'12分钟前')
    print timestamp2datetime(1484257158)
