import numpy as np
import time
import cv2
import matplotlib.pyplot as plt
def threshold(img):
    img1 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    img2 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    frame = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    ret, imgBinary = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # ret, imgBinary = cv2.threshold(frame, 80, 255,cv2.THRESH_BINARY)
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

    # imgContour = cv2.drawContours(img1, contours[0:len(contours)],-1, (0,0,255), 2)
    print(f'chieu cao:{height[:]}')
    # sortHeight = sorted(h)
    print(f'ret:{ret}') 

    a = int(2.7)
    print(a)
    titles = ['original image', 'grey' , 'imgBinary', 'draw contour']
    images = [img2, frame, imgBinary ]
    # for i in range(4):
    #     plt.subplot(2, 2, i+1)
    #     plt.title(titles[i])
    #     plt.imshow(images[i], 'gray')


    plt.show()
    imgBinary = cv2.resize(img1, (780,550))
    # cv2.imshow("image", imgBinary)
    # cv2.imshow("image", img)
    cv2.imshow("image", imgBinary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\40cm_test2.jpeg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\Led_tach_RoI.jpeg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID-cheo2.jpeg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID_4LED_10_07.jpg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LEDID_4_RoI_adjusted.jpg")
img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID_long.jpeg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\3_led.jpg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LEDID_3_RoI.jpeg")
# img = img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID_newphone.png")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\40cm_test2.jpeg")


threshold(img)


