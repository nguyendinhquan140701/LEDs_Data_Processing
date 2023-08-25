import numpy as np
import time
import cv2
import matplotlib.pyplot as plt
from collections import Counter
def threshold(img):
    # img1 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # img2 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)

    select1 = frame[frame > 10]
    print(f"{select1[:]}")
    avgValue = np.mean(select1)
    print(f"avg pixel value: {avgValue}")

    print(f'frame: {frame[0:200]}')
    width = frame.shape[1]
    ret, imgBinary = cv2.threshold(blurred, avgValue, 255,cv2.THRESH_BINARY)
    contours, hierachy = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(f"len(contours):{len(contours)}")
    for i in range (0, len(contours)):
        x,y,w,h = cv2.boundingRect(contours[i])
        rect = cv2.minAreaRect(contours[i])
        center, size, angle = rect
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        img1 = cv2.drawContours(img,[box],0,(0,0,255),2)

        print(f"center, size, angle:{center}, {size}, {angle}")
    imgShow = cv2.resize(img1, (780,550))

    cv2.imshow("image", imgShow)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\40cm_test2.jpeg")
img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\Led_long_cheo2.jpg")



threshold(img)