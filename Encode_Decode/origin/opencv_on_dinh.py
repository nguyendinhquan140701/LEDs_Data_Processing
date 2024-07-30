# import the opencv library
import cv2
import ham_check_roi_tu_arr_6_5 as hc
import ham_ve_roi_4 as hvr
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import ham_xu_ly_anh_xam as hxla
import ham_xu_ly_y_4 as xly
import time


st = time.time()

vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_EXPOSURE, -13)
vid.set(3, 640)
vid.set(4, 480)
# array2 = [[0]]
bien_nho_max = 0
bien_nho_so_anh = 0
mang_so_1 =[0]
mang_so_1_append = []

while(True):

    array2 = [[0]] # TH khong can tinh xac suat
    ret, img = vid.read()
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #
#    cv2.imshow("Frame", img) # raw


#    height = frame.shape[0]
    width = frame.shape[1]
#     print("height, width", height, width)

    ret, frame0 = cv2.threshold(frame, 200, 255, cv2.THRESH_BINARY)
#    cv2.imshow("Frame", frame0)
    contours, hierarchy = cv2.findContours(frame0, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
    if len(contours) >= 500 or len(contours) <= 10000:
        contours = contours[0:len(contours):250]
    if len(contours) == 0 or len(contours) > 10000:
        pass

    # print(contours)


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

        print("lennnnnnn",len(contours))

        
    # if len(contours) == 0 or len(contours) >= 50:
    #    pass
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
        if a[0] == a[1] == a[2] == a[3] ==0 or abs(a[1]-a[3]>=480) or a[1] == 480 or [a3] == 480: #ok fix 480
            a = [0,0,0,103]
        if b[0] == b[1] == b[2] == b[3] ==0 or abs(a[1]-a[3]>=480):
            b = [0,0,0,103]

        print("roi1,roi2", a,b)

        text1 = 'RoI'
#        text2 = 'r2'
        x = width
        frame2 = hvr.ve_roi(img, text1, a, x) 
#        frame2 = hvr.ve_roi(img, text2, b, x)



#-----------------------------------------------------------------------------
        Npixel = 4

        array = a


        a0,b0,c0,d0 = hxla.xu_ly_anh(frame, array, Npixel)

#        print("Kich thuoc cua line", a0)
#        plt.plot(f0, b0) 
#        plt.show()
#        print('output_variable = Array out = decimated array: ', c0)
#        print("size(s): ", d0)
#        plt.plot(e0, b0)
#        plt.show()

        
        values_y = c0
        row = 100
        threshold_code = [0,1,1,1,0,0,1,0,0,1]
        input_var = 4

        a00, a1, a2, a3, a4, a5, a6, a7, a8, a9 = xly.xu_ly_y(array2, values_y, row, threshold_code, input_var)

#        print("threshold: ",a00)
#        print("số mẫu: ", a1)
#        print("data matrix: ", a2)
#        print("Array: ", a3)
#        plt.plot(a4, a5)
#        plt.show()
##        print("xac suat nhan dang dung cua den 1:", int(a6))
#        print("so lan xuat hien:", a7)
##        print("du lieu giai ma tu den", a8, "\n")
        
#        print("so hang lay duoc: ", a9)

        if a8 == threshold_code[len(threshold_code)-input_var:len(threshold_code)]:
            mang_so_1_append = 1
        else:
            mang_so_1_append = 0
        mang_so_1 = np.append(mang_so_1_append, mang_so_1)


        
##        print('mang_so_1', mang_so_1)


        if len(mang_so_1) <= row-1:
            mang_so_1 = mang_so_1

        else:
            mang_so_1 = mang_so_1[0:row]
        tong_so_1 = np.count_nonzero(mang_so_1 == 1)
        
        a6 = (tong_so_1)*100/len(mang_so_1)
##        print('tong_so_1', tong_so_1)
##
##
##        print('len_mang_so_1', len(mang_so_1))
##        
        
##        print('array2', array2)
##        if len(a3) <= row:
##            array2 = a3
##        else:
##            array2 = a3[0:row]
        bien_nho_so_anh = bien_nho_so_anh + 1
#        if aa == 600:
##        print(bien_nho_so_anh)
        # Display the resulting frame
#        cv2.imshow('frame', img)
#---------------------------------------------------------------
# xu ly bien nho:
        if a6 > bien_nho_max:
            bien_nho_max = a6
#        print("bien nho", a6)
#---------------------------------------------------------------

        font = cv2.FONT_HERSHEY_SIMPLEX

        frame2= cv2.putText(frame2, "Xac suat nhan dang dung cua den (%):", (0,385),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
        frame2= cv2.putText(frame2, str(int(a6)), (10,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)

        frame2= cv2.putText(frame2, "(max", (45,410),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu

        frame2= cv2.putText(frame2, str(int(bien_nho_max)), (100,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)
        frame2= cv2.putText(frame2, ")", (140,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)



        
        
        frame2= cv2.putText(frame2, "Du lieu giai ma tu den:", (0,450),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
        frame2= cv2.putText(frame2, str(a8), (10,475),font, 0.7, (0,0,255),2,cv2.LINE_AA)


        frame2= cv2.putText(frame2, "So anh da xu ly:", (450,450),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
        frame2= cv2.putText(frame2, str(bien_nho_so_anh), (460,475),font, 0.7, (0,0,255),2,cv2.LINE_AA)
        et = time.time()
 
        elapsed_time = round(et - st,2)

        frame2= cv2.putText(frame2, "Thoi gian (s):", (450, 385),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
        frame2= cv2.putText(frame2, str(elapsed_time), (460,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)



        cv2.imshow("Frame", frame2)
        

        if cv2.waitKey(1) & 0xFF == ord('p'):
            cv2.waitKey(-1)

 

        # get the execution time

#        print('time', elapsed_time)

    vid.release()
    cv2.destroyAllWindows()

#--------------------------------------------------
# xóa comment thừa ok
# xóa height: ok
# sửa tối ưu vào module xla ok
# xóa đặt trùng tên ok
# xóa các lệnh thừa trùng lặp
# chỉnh xla xám về 100 để không bị lỗi, đặt lại đ.kiện N
