# coding:utf8

__author__ = 'HuijunZhang'


class CommonParser():
    def __init__(self):
        pass

    def trim(self, string):
        if not string:
            return string
        string = string.replace(u'\r', u'').replace(u'\n', u'').replace(u'\t', u'')
        return string.strip()


if __name__ == '__main__':
    print CommonParser().trim('dasNo')
