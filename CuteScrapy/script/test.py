# coding:utf8
import os

import re


class Scan():
    def __init__(self):
        pass


    def scanFile(self,output):
        smaliList = []
        for parent, dirnames, filenames in os.walk(output):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:  # 输出文件信息
                smaliList.append(os.path.join(parent, filename))
        return smaliList

    def checkIP(self,list):
        for _file in list:
            data = self.getDataFromFile(_file)
            # result = re.search('\d+\.\d+\.\d+\.\d+',data)
            result = re.search('port',data)
            if result != None:
                print _file

    def getDataFromFile(self, path):
        with open(path, 'r') as f:
            data = f.read()
            f.close()
        return data

    def run(self):
        list = self.scanFile('/Users/huijunzhang/Documents/58cheshangtong/58cheshangtong/air/com/wuba/cardealertong')
        self.checkIP(list)

if __name__ == '__main__':
    Scan().run()