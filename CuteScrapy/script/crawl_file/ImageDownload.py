# coding:utf8
import os
import hashlib
import datetime
from lxml import etree
import requests

# 文件下载脚本

file_folder = {
    '.jpg': 'image',
    '.png': 'image',
    '.jpeg': 'image',
    '.gif': 'image',
    '.bmp': 'image',
    '.ico': 'image',
    '.txt': 'doc',
    '.page': 'doc',
    '.doc': 'doc',
    '.docx': 'doc',
    '.key': 'doc',
    '.ppt': 'doc',
    '.pptx': 'doc',
    '.pdf': 'doc',
    '.html': 'web',
    '.css': 'web',
    '.js': 'web'
}


class ImageDownload():
    def __init__(self):
        pass

    def getParams(self, url, site, default_suffix):
        '''
        获取文件类型,保存文件名,保存路径
        :param url:保存文件的地址
        :param site:站点
        :param default_suffix:默认后缀(eg:".html")
        :return:json
        '''
        file_name = os.path.basename(url)
        suffix = os.path.splitext(url)[-1] or default_suffix
        file_name = file_name if file_name.find('.') > -1 else ("%s%s" % (hashlib.md5(url).hexdigest(), suffix))
        file_type = file_folder.get(suffix, 'other')
        file_path = '%s/%s/%s' % (site, file_type, file_name) if site else '%s/%s' % (file_type, file_name)
        return {
            "file_type": file_type,
            "file_name": file_name,
            "file_path": file_path
        }

    def download_file(self, file_url, site, default_suffix=None):
        if not file_url:
            return
        ds = datetime.datetime.now().strftime('%Y-%m-%d')
        params = self.getParams(file_url, site=site, default_suffix=default_suffix)
        params['file_path'] = '%s/%s' % (ds, params['file_path'])

        file_dir = params['file_path'].replace(params['file_name'], '')
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)  # 文件夹不存在创建文件夹

        file_path = params.get('file_path')
        if file_url.find('http') <= -1:
            file_url = 'http:%s' % file_url
        sz = open(file_path, 'wb').write(requests.get(file_url).content)
        return file_path

    def crawl_pic(self, page_url, site):
        response = requests.get(page_url)
        tree = etree.HTML(response.text)
        src_li = tree.xpath('//img')
        for img in src_li:
            image = img.get('src2') or img.get('data-src') or img.get('src')
            print image
            self.download_file(image, site, default_suffix='.png')
        print response


if __name__ == '__main__':
    # url = 'http://car.autohome.com.cn/photolist/spec/21776/p1/'
    url = 'https://mp.weixin.qq.com/s?__biz=MjM5NTQ5Mjk4MA==&mid=2652727552&idx=7&sn=5d763df699abe269f37bda1b3755c9db&scene=0#wechat_redirect'
    ImageDownload().crawl_pic(url,'weixin')
