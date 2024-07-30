import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
import math
import sys
sys.path.append('E:\Project\OOC\LEDs_Data_Processing\LED_Decode')

class test_Dong:
    def __init__(self):

        self.image = cv2.imread('E:\Project\OOC\LEDs_Data_Processing\LED_Decode\led_image\\40cm_test2.jpeg')
    def process_frame(self, focallengthkt, pixelsizekt, azimuthkt, pitchkt, rollkt):
        try:
            img = self.image
            heightpy, widthpy, _ = img.shape
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            print(f"focallengthis:{focallengthkt}")
            print(f"pixelsizeis:{pixelsizekt}")
            # Áp dụng phép xử lý ngưỡng để chuyển đổi ảnh thành ảnh nhị phân
            _, thresholdpy = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

            # Tìm các đường viền trong ảnh nhị phân
            contourspy, _ = cv2.findContours(thresholdpy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            topmost1 = None
            bottommost1 =None

            # Lặp qua tất cả các đường viền
            for contourpy in contourspy:
                # Lấy tọa độ pixel của điểm cao nhất và thấp nhất của đường viền hiện tại
                current_topmost = tuple(contourpy[contourpy[:, :, 1].argmin()][0])
                current_bottommost = tuple(contourpy[contourpy[:, :, 1].argmax()][0])

                # Cập nhật tọa độ pixel của điểm cao nhất và thấp nhất nếu cần
                if topmost1 is None or current_topmost[1] < topmost1[1]:
                    topmost1 = current_topmost
                    bottommost1 = current_bottommost


            def tinhtoado(diemcaonhat, diemthapnhat, pixelwidth, pixelheight):
                xtamanh = pixelwidth/2
                ytamanh = pixelheight/2
                xtamden = (diemcaonhat[0] + diemthapnhat[0])/2
                ytamden = (diemcaonhat[1] + diemthapnhat[1])/2
                xdelta = xtamden - xtamanh
                ydelta = ytamden - ytamanh
                dodaipixelanh = math.sqrt((diemthapnhat[0] - diemcaonhat[0])**2 + (diemthapnhat[1] - diemcaonhat[1])**2)
                goclech = math.atan2(ydelta,xdelta)

                print(f"goclechis:{goclech}")

                # khoangcachthuc = 10*math.sqrt(xdelta**2 + ydelta**2)/dodaipixelanh
                # ztoado = 275 - 10*focallength/(dodaipixelanh*pixelsize)
                # print(f"ztoadois:{pixelsize}")
                # print(f"ytoadois:{dodaipixelanh}")
                # xtoado = khoangcachthuc*math.cos(math.pi - goclech)
                # ytoado = khoangcachthuc*math.sin(math.pi - goclech)
                # return (xtoado,ytoado,ztoado)

            # def xoaytruc(toado,azimuth,pitch,roll):
            #     matrixR = np.array([
            #         [np.cos(azimuth)*np.cos(roll), -np.sin(azimuth)*np.cos(pitch), np.cos(azimuth)*np.sin(roll)+np.sin(azimuth)*np.sin(pitch)*np.cos(roll)],
            #         [np.sin(azimuth)*np.cos(roll), np.cos(azimuth)*np.cos(pitch), np.sin(azimuth)*np.sin(roll)-np.cos(azimuth)*np.sin(pitch)*np.cos(roll)],
            #         [-np.cos(pitch)*np.sin(roll), np.sin(pitch), np.cos(pitch)*np.cos(roll)]
            #     ])
            #     matrixA = np.array([[toado[0]],[toado[1]],[toado[2]]])
            #     matrixB = np.linalg.inv(matrixR) @ matrixA
            #     return matrixB
            
        except:
            print("Error")

if __name__ == "__main__":
    test = test_Dong()
    test.process_frame(20, 0.1, 0, 0, 0)