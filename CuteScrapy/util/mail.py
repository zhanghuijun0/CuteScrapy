# coding:utf8
from scrapy import settings
from scrapy.mail import MailSender

__author__ = 'HuijunZHang'


def sendEmail():
    mailer = MailSender.from_settings(settings)

    # mailer.send(['zhanghuijun@souche.com'], 'test_subject', 'hello', cc=None, attachs=(), mimetype='text/plain')

    # mailer.send(to=["zhanghuijun@souche.com"], subject="Some subject", body="Some body", cc=["zhanghuijun@souche.com"])

    print 'ss'



if __name__ == '__main__':
    sendEmail()
