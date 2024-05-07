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

    select1 = frame[frame > 10]
    print(f"{select1[:]}")
    avgValue = np.mean(select1)
    print(f"avg pixel value: {avgValue}")

    print(f'frame: {frame[0:200]}')
    width = frame.shape[1]

    # ret, imgBinary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ret, imgBinary = cv2.threshold(blurred, avgValue, 255,cv2.THRESH_BINARY)
    # imgBinary = cv2.adaptiveThreshold(frame, 255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 41, 15)
    # print(f"ret:{ret}")
    contours, hierachy = cv2.findContours(imgBinary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    height = []
    top = []
    bot = []
    areas = []
    before_contours_sort = []
    len_all_contours = []
    # print(f'contours:{contours[0]} ')

    # print(f'before_contour_sort:{before_contours_sort[0:13]}')
    # print(f'len_all_contours:{len_all_contours[:]}')

    for i in range (0, len(contours)):
        x,y,w,h = cv2.boundingRect(contours[i])
        top.append(int(y))
        bot.append(int(y+h))
        height.append(int(h))
        # cv2.rectangle(img1,(x,y),(x+w,y+h),(0,0,255),2)
    
    # cv2.rectangle(img1,(x,y),(x+w,y+h),(0,0,255),2)
    sort_height = sorted(height, reverse=True)
    Npixel = int(sort_height[0]/3)
    print(f'Npixel:{Npixel}')
    print(f'sort_height:{sort_height}')

    contours_final = []
    for i in range(0, len(contours)):
        if cv2.contourArea(contours[i]) > 5*Npixel:
            contours_final.append(contours[i])
        else:
            pass

    len_all_contours_final=[]
    for i in range(0, len(contours_final)):
        before_contours_sort.append(cv2.contourArea(contours_final[i]))
        len_all_contours_final.append(len(contours_final[i]))
    
    print(f'before_contourfinal_sort:{before_contours_sort[0:13]}')
    print(f'len_all_contours_final:{len_all_contours_final[:]}')

    top_final = []
    bot_final = []
    height_final = []

    for i in range (4, 5) and (4, 7) :
        x_final,y_final,w_final,h_final = cv2.boundingRect(contours_final[i])
        top_final.append(int(y_final))
        bot_final.append(int(y_final+h_final))
        height_final.append(int(h_final))
        cv2.rectangle(img1,(x_final,y_final),(x_final+w_final,y_final+h_final),(0,0,255),2)
    print(f'x_final:{x_final}\ny_final:{y_final}')
    # cv2.rectangle(img1,(x_final[4],y_final[4]),(x_final[4]+w_final[4],y_final[4]+h_final[4]),(0,0,255),2)
    print(f'chieu cao:{height_final[:]}')
    frequency_map = Counter(height_final)

    # Sắp xếp từ điển theo giá trị (value) từ lớn đến nhỏ
    sorted_frequency_map = dict(sorted(frequency_map.items(), key=lambda item: item[1], reverse=True))

    # In ra key có value lớn nhất và giá trị tương ứng
    most_frequent_key = next(iter(sorted_frequency_map))
    most_frequent_value = sorted_frequency_map[most_frequent_key]
    print(f"Key có value lớn nhất: {most_frequent_key}, với tần suất xuất hiện: {most_frequent_value}")

    imgContour = cv2.drawContours(img1, contours_final[:],-1, (0,0,255), 2)

    # sortHeight = sorted(h)
    print(f'ret:{ret}') 


    # cv2.imwrite('blur_image.png', imgBinary)
    cv2.imwrite('grey_image.png', imgBinary)
    plt.show()
    imgShow = cv2.resize(imgBinary, (780,550))

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
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID-GN2200_4000Hz.jpg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\GN2200\\6.jpg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\zoom_pixel4.jpg")





threshold(img)


