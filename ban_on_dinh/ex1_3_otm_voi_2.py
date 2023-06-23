# import the opencv library
import cv2
import ham_check_roi_tu_arr_6_5 as hc
import ham_ve_roi_4 as hvr
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import ham_xu_ly_anh_xam as hxla
import ham_xu_ly_y_4 as xly


vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_EXPOSURE, -14)
array2 = [[0]]
aa = 0

while(True):


    ret, img = vid.read()
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #
#    cv2.imshow("Frame", img) # raw


#    height = frame.shape[0]
    width = frame.shape[1]
#     print("height, width", height, width)

    ret, frame0 = cv2.threshold(frame, 230, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(frame0, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print("len contours: ", len(contours))
    if len(contours) > 0 and len(contours)<=40:
        contours = contours
    if len(contours) > 40 and len(contours)<100:
        contours = contours[0:len(contours):2]
    if len(contours) >= 100 and len(contours)<150:
        contours = contours[0:len(contours):3]
    if len(contours) >= 150 and len(contours)<200:
        contours = contours[0:len(contours):4]
    if len(contours) >= 200 and len(contours)<300:
        contours = contours[0:len(contours):7]
    if len(contours) >= 300 and len(contours)<500:
        contours = contours[0:len(contours):10]
    if len(contours) >= 500 and len(contours) < 700:
            contours = contours[0:len(contours):15]
    if len(contours) >= 700 and len(contours) < 1000:
        contours = contours[0:len(contours):25]
    if len(contours) >= 1000 and len(contours) < 1300:
        contours = contours[0:len(contours):30]
    # print("lennnnnnn6",len(contours))
    if len(contours) >= 1300 and len(contours) < 1800:
        contours = contours[0:len(contours):40]
    if len(contours) == 0 or len(contours) > 10000:
            print("contour over")

    mass_centres_x = []
    mass_centres_y = []
    top = []
    bot = []

    for i in range(0, len(contours)):
        M = cv2.moments(contours[i], 0)
        if M["m00"] != 0:
            mass_centres_x.append(int(M['m10']/M['m00']))
            mass_centres_y.append(int(M['m01']/M['m00']))
        else:
            mass_centres_x.append(int(0))
            mass_centres_y.append(int(0))

    for i in range(0, len(contours)):
        x,y,w,h = cv2.boundingRect(contours[i])
        cv2.rectangle(frame0,(x,y),(x+w,y+h),(255,0,0),2)
        top.append(int(y))
        bot.append(int(y+h))
    if len(contours) == 0 or len(contours) > 50:
        pass
    else:
        if len(mass_centres_x) == 0:
           mass_centres_x = np.zeros(5, dtype=int)
        if len(mass_centres_y) == 0:
           mass_centres_y = np.zeros(5, dtype=int)
        if len(top) == 0:
           top = np.zeros(5, dtype=int)
        if len(bot) == 0:
           bot = np.zeros(5, dtype=int)

        a, b = hc.check_roi_tu_arr(mass_centres_x, mass_centres_y, top, bot)
        if a[0] == a[1] == a[2] == a[3] ==0 or abs(a[1]-a[3]>=480) or a[1] == 480 or a[3] == 480:
            a = [0,0,0,103]
        if b[0] == b[1] == b[2] == b[3] ==0 or abs(b[1]-b[3]>=480) or b[1] == 480 or b[3] == 480:
            b = [0,0,0,103]
#        print("roi1,roi2", a,b)

        text1 = 'RoI1'
        text2 = 'RoI2'
        x = width
        frame2 = hvr.ve_roi(img, text1, a, x) 
        frame2 = hvr.ve_roi(img, text2, b, x) 

        cv2.imshow("Frame", frame2)
#-----------------------------------------------------------------------------
        Npixel = 4

        array = a
        array_0 = b

        a0,b0,c0,d0,e0,f0 = hxla.xu_ly_anh(frame, array, Npixel)
        a0_0,b0_0,c0_0,d0_0,e0_0,f0_0 = hxla.xu_ly_anh(frame, array_0, Npixel)

#        print("Kich thuoc cua line", a0)
#        plt.plot(f0, b0) 
#        plt.show()
#        print('output_variable = Array out = decimated array: ', c0)
#        print("size(s): ", d0)
#        plt.plot(e0, b0)
#        plt.show()

        
        values_y = c0
        values_y_0 = c0_0
        row = 100
        threshold_code = [0,1,1,1,0,0,1,0,0,1]
        input_var = 4

        a00, a1, a2, a3, a4, a5, a6, a7, a8, a9 = xly.xu_ly_y(array2, values_y, row, threshold_code, input_var)
        a00_0, a1_0, a2_0, a3_0, a4_0, a5_0, a6_0, a7_0, a8_0, a9_0 = xly.xu_ly_y(array2, values_y_0, row, threshold_code, input_var)

        

#        print("threshold: ",a00)
#        print("số mẫu: ", a1)
#        print("data matrix: ", a2)
#        print("Array: ", a3)
#        plt.plot(a4, a5)
#        plt.show()
        print("sac xuat1:", a6)
        print("sac xuat2:", a6_0)
        
#        print("so lan xuat hien:", a7)
        print("data nhan duoc theo bit", a8)
        print("data nhan duoc theo bit", a8_0)
#        print("so hang lay duoc: ", a9)

        if len(a3) <= row:
            array2 = a3
        else:
            array2 = a3[0:row]
        aa = aa + 1
        if aa == 600:
            print(aa)
        # Display the resulting frame
#        cv2.imshow('frame', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
  

vid.release()
cv2.destroyAllWindows()

#--------------------------------------------------
# xóa comment thừa ok
# xóa height: ok
# sửa tối ưu vào module xla ok
# xóa đặt trùng tên ok
# xóa các lệnh thừa trùng lặp
# chỉnh xla xám về 100 để không bị lỗi, đặt lại đ.kiện N
