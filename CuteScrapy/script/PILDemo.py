# coding=utf-8
# !/usr/bin/env python

import cv2
from cv2 import cv
import numpy as np
from pylab import *
import glob
import os

# i = 0
# for files in glob.glob('/Users/huijunzhang/Desktop/4002.jpg'):
#     filepath, filename = os.path.split(files)
#     image = cv2.imread(filepath + '/' + filename)
#     # image = cv2.imread('D:/pic/car2.jpg')
#     h, w = image.shape[:2]
#     # 灰度化
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     grayIPimage = cv.GetImage(cv.fromarray(gray))
#     sobel = cv.CreateImage((w, h), cv2.IPL_DEPTH_16S, 1)  # 创建一张深度为16位有符号（-65536~65535）的的图像区域保持处理结果
#     cv.Sobel(grayIPimage, sobel, 2, 0, 7)  # 进行x方向的sobel检测
#     temp = cv.CreateImage(cv.GetSize(sobel), cv2.IPL_DEPTH_8U, 1)  # 图像格式转换回8位深度已进行下一步处理
#     cv.ConvertScale(sobel, temp, 0.00390625, 0)
#     cv.Threshold(temp, temp, 0, 255, cv2.THRESH_OTSU)
#     kernal = cv.CreateStructuringElementEx(3, 1, 1, 0, 0)
#     cv.Dilate(temp, temp, kernal, 2)
#     cv.Erode(temp, temp, kernal, 4)
#     cv.Dilate(temp, temp, kernal, 2)
#     #     cv.ShowImage('1', temp)
#     kernal = cv.CreateStructuringElementEx(1, 3, 0, 1, 0)
#     cv.Erode(temp, temp, kernal, 1)
#     cv.Dilate(temp, temp, kernal, 3)
#     #     cv.ShowImage('2', temp)
#     temp = np.asarray(cv.GetMat(temp))
#     contours, heirs = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     for tours in contours:
#         rc = cv2.boundingRect(tours)
#         if rc[2] / float(rc[3]) >= 3:
#             print rc[2] / float(rc[3])
#             # rc[0] 表示图像左上角的纵坐标，rc[1] 表示图像左上角的横坐标，rc[2] 表示图像的宽度，rc[3] 表示图像的高度，
#             cv2.rectangle(image, (rc[0], rc[1]), (rc[0] + rc[2], rc[1] + rc[3]), (255, 0, 255))
#             imageIp = cv.GetImage(cv.fromarray(image))
#             cv.SetImageROI(imageIp, rc)
#             imageCopy = cv.CreateImage((rc[2], rc[3]), cv2.IPL_DEPTH_8U, 3)
#             cv.Copy(imageIp, imageCopy)
#             cv.ResetImageROI(imageIp)
#             # cv.SaveImage('/Users/huijunzhang/Desktop/' + str(i) + '.jpg', imageCopy)
#             # i = i + 1
# cv2.imshow("黑底白字",image)
# print '----'
# cv2.waitKey(0)  # 暂停用于显示图片
# cv2.destroyAllWindows()
def run():
    file_name = '/Users/huijunzhang/Desktop/4002.jpg'
    img = cv2.imread(file_name,cv2.IMREAD_GRAYSCALE)
    cv2.imshow('image',img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

run()