import numpy as np
import time
import cv2
import matplotlib.pyplot as plt
from collections import Counter
def threshold(img):
    img1 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img2 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    frame = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)

    select1 = blurred[blurred > 10]
    print(f"{select1[:]}")
    avgValue = np.mean(select1)
    print(f"avg pixel value: {avgValue}")


    print(f'frame: {frame[0:200]}')
    width = frame.shape[1]

    # ret, imgBinary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ret, imgBinary = cv2.threshold(blurred, avgValue, 255,cv2.THRESH_BINARY)
    # thresh = cv2.adaptiveThreshold(frame, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 5)
    print(f"ret:{ret}")
    contours, hierachy = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    height = []
    top = []
    bot = []
    for i in range(0, len(contours)):
        x,y,w,h = cv2.boundingRect(contours[i])
        top.append(int(y))
        bot.append(int(y+h))
        height.append(int(h))
        cv2.rectangle(img1,(x,y),(x+w,y+h),(0,0,255),2)

    sort_height = sorted(height, reverse=True)
    print(f'sort_height:{sort_height}')

    frequency_map = Counter(height)

    # Sắp xếp từ điển theo giá trị (value) từ lớn đến nhỏ
    sorted_frequency_map = dict(sorted(frequency_map.items(), key=lambda item: item[1], reverse=True))

    # In ra key có value lớn nhất và giá trị tương ứng
    most_frequent_key = next(iter(sorted_frequency_map))
    most_frequent_value = sorted_frequency_map[most_frequent_key]
    print(f"Key có value lớn nhất: {most_frequent_key}, với tần suất xuất hiện: {most_frequent_value}")

    # imgContour = cv2.drawContours(img1, contours[0:len(contours)],-1, (0,0,255), 2)
    print(f'chieu cao:{height[:]}')
    # sortHeight = sorted(h)
    # print(f'ret:{ret}') 

    a = int(2.7)
    print(a)

    # cv2.imwrite('blur_image.png', imgBinary)
    cv2.imwrite('grey_image.png', imgBinary)
    plt.show()
    imgShow = cv2.resize(img1, (780,550))

    # cv2.imshow("image", imgBinary)
    # cv2.imshow("image", img)
    cv2.imshow("image", imgShow)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\40cm_test2.jpeg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\Led_tach_RoI.jpeg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID-cheo2.jpeg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID_4LED_10_07.jpg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LEDID_4_RoI_adjusted.jpg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID_long.jpeg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\3_led.jpg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LEDID_3_RoI.jpeg")
# img = img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID_newphone.png")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\test7.jpeg")



threshold(img)


