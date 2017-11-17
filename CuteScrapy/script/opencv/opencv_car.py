# coding:utf8
import random
import cv2
import numpy as np


class Main():

    def __init__(self):
        pass

    def colorDetect(self, image, option=0):
        # name = random.randint(0, 99)
        img = cv2.imread(image)
        colorImage = img.copy()
        _colorImage = img.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # 高斯模糊
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # 设定蓝色的阈值
        if (option == 0):
            lower = np.array([190, 50, 50])
            upper = np.array([245, 255, 255])
        else:
            # 黄色
            lower = np.array([15, 50, 50])
            upper = np.array([40, 255, 255])

        # 根据阈值构建掩模
        mask = cv2.inRange(hsv, lower, upper)
        # 对原图像和掩模进行位运算
        res = cv2.bitwise_and(img, img, mask=mask)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        # 二值化
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # 闭操作
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 3))
        closed = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
        (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # boxes = choose(cnts)
        cv2.drawContours(img,cnts,-1,(0,0,255),1)
        cv2.imshow("title:" + str(random.randint(0, 99)), img)
        cv2.waitKey(0)
        imgRs = []
        i = 0
        for cnt in cnts:
            rect = cv2.minAreaRect(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            if (w < 50 or h < 15 or w > h < 1.0):
                continue
            # cv2.rectangle(_colorImage,(x,y),(x+w,y+h),(0,255,0),1)
            # imgCrop = _colorImage[y:y+h,x:x+w]
            imgRs.append((x, y, w, h, rect[2]))
            rs = img[y:y + h, x:x + w]
            cv2.imshow("title:"+str(random.randint(0,99)),rs)
            cv2.waitKey(0)

        # cv2.drawContours(_colorImage, [_box], -1, (0,0,255), 1)
        # cv2.imshow("_colorImage",_colorImage)

        return imgRs


# from openalpr import Alpr
#
# alpr = Alpr("us", "/path/to/openalpr.conf", "/path/to/runtime_data")
# if not alpr.is_loaded():
#     print("Error loading OpenALPR")
#     sys.exit(1)
#
# alpr.set_top_n(20)
# alpr.set_default_region("md")
#
# results = alpr.recognize_file("/path/to/image.jpg")
#
# i = 0
# for plate in results['results']:
#     i += 1
#     print("Plate #%d" % i)
#     print("   %12s %12s" % ("Plate", "Confidence"))
#     for candidate in plate['candidates']:
#         prefix = "-"
#         if candidate['matches_template']:
#             prefix = "*"
#
#         print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

# Call when completely done to release memory
alpr.unload()

if __name__ == '__main__':
    print Main().colorDetect('1.jpg')