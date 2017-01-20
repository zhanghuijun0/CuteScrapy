# coding:utf8
import zbar
from PIL import Image
import urllib
import cStringIO
__author__ = 'HuijunZhang'

class ScrannerQrcodeHelper():
    def __init__(self):
        pass

    def getContentFromQrcode(self,url):
        result = []
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
        return result


if __name__ == '__main__':
    # print 'hello'
    print ScrannerQrcodeHelper().getContentFromQrcode('http://article.fd.zol-img.com.cn/t_s640x2000/g3/M04/0A/08/Cg-4V1Q86VuINu4gAATjuEp6SzcAAQHcwAWcdIABOPQ167.jpg')
    # ScrannerQrcodeHelper().getContentFromQrcode('http://blog.zhanghuijun.site/img/avatar.png')
    # ScrannerQrcodeHelper().getContentFromQrcode('http://media.ifanrusercontent.com/media/user_files/trochili/fc/33/fc331f37618456dad00d5f5395f8fe0780653d97-18a9aa58f7e126d2fbfe091d2ecc0dffc15b6225.jpg,http://media.ifanrusercontent.com/media/user_files/trochili/80/7a/807a8e2386235808deb426aec4bf8ff03cba8c27-7e375f76c28c5aabf29e62e79f9d7bd1545aa6fe.jpg')
    print ScrannerQrcodeHelper().getContentFromQrcode('http://media.ifanrusercontent.com/media/user_files/trochili/58/4a/584a5a39479c7cc3f75b54d5ff58d7bab677df17-09ce9753ea1ebfe7b5ca9a9b8a44feefc34e6451.png')