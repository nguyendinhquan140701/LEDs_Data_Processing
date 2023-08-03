# import the opencv larray2ibrary
import cv2
# import ham_check_roi_tu_arr_6_5 as hc
# import ham_ve_roi_4 as hvr
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math as goc_lech
import time
# import ham_xu_ly_anh_xam as hxla
# import ham_xu_ly_y_4 as xly



# vid = cv2.VideoCapture(0)
# vid.set(cv2.CAP_PROP_EXPOSURE, -13)
# vid.set(3, 640)
# vid.set(4, 480)
array2 = [[0]]
aa = 0
def process_frame(img):
# while(True):
    start_time_total = time.time()
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)   
    # ret, img = vid.read()
    frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #

    select = frame[frame > 0]
    avg = np.mean(select)
    print(f"avg pixel value: {avg}")
    #    cv2.imshow("Frame", img) # raw


    height = frame.shape[0]
    width = frame.shape[1]
    #     print("height, width", height, width)

    ret, frame0 = cv2.threshold(frame, 80, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(frame0, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print("len contours: ", len(contours))
    if len(contours) > 0 and len(contours)<=60:
        contours = contours
    if len(contours) > 60 and len(contours)<90:
        contours = contours[0:(len(contours)-30)]
    if len(contours) >= 90 and len(contours)<100:
        contours = contours[0:len(contours):2]
    if len(contours) >= 100 and len(contours)<150:
        contours = contours[0:len(contours):5]
    if len(contours) >= 150 and len(contours)<200:
        contours = contours[0:len(contours):7]
    if len(contours) >= 200 and len(contours)<300:
        contours = contours[0:len(contours):9]
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
    print("len contours: ", len(contours))
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
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        top.append(int(y))
        bot.append(int(y+h))
    if len(contours) == 0 or len(contours) > 60:
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


        Npixel = 8
        # Npixel = 11
        # Npixel = 4

        # a, b = hc.check_roi_tu_arr(mass_centres_x, mass_centres_y, top, bot)

        a, b, c, d, time_checkRoI = check_roi_tu_arr(mass_centres_x,mass_centres_y, top, bot, Npixel)
        # print(f"gia tri a[1] va a[3], hieu a[1] va a[3]: {a[1]} va {a[3]} va hieu:{abs(a[1] - a[3])}")
        if a[0] == a[1] == a[2] == a[3] ==0 or abs(a[1]-a[3]>=480) or a[1] == 480 or a[3] == 480:
            a = [0,0,0,103]
            # print(a)
        if b[0] == b[1] == b[2] == b[3] ==0 or abs(b[1]-b[3]>=480) or b[1] == 480 or b[3] == 480:
            b = [0,0,0,103]
        if c[0] == c[1] == c[2] == c[3] ==0 or abs(c[1]-c[3]>=480) or c[1] == 480 or c[3] == 480:
            c = [0,0,0,103]
        if d[0] == d[1] == d[2] == d[3] ==0 or abs(d[1]-d[3]>=480) or d[1] == 480 or d[3] == 480:
            d = [0,0,0,103]
        print(f"roi1: {a}, roi2: {b}, roi3: {c}, roi4: {d}")

        text1 = 'RoI1'
        text2 = 'RoI2'
        text3 = 'RoI3'
        text4 = 'RoI4'
        x = width
        # frame2 = hvr.ve_roi(img, text1, a, x) 
        # frame2 = hvr.ve_roi(img, text2, b, x) 
        frame2, time_veRoi1 = ve_roi(img, text1, a, x)
        frame2, time_veRoi2 = ve_roi(img, text2, b, x)
        frame2, time_veRoi3 = ve_roi(img, text3, c, x)
        frame2, time_veRoi4 = ve_roi(img, text4, d, x)

        # cv2.imshow("Frame", frame2)
        frame2 = img    
        
    #-----------------------------------------------------------------------------
        
        # frame = img
        array = a
        array_0 = b
        array_1 = c
        array_2 = d

        # a0,b0,c0,d0 = hxla.xu_ly_anh(frame, array, Npixel)
        # a0_0,b0_0,c0_0,d0_0 = hxla.xu_ly_anh(frame, array_0, Npixel)
        a0,b0,c0,d0, time_xuLyLine1 = xu_ly_anh(frame, array, Npixel)
        a0_0,b0_0,c0_0,d0_0, time_xuLyLine2 = xu_ly_anh(frame, array_0, Npixel)
        a0_1,b0_1,c0_1,d0_1, time_xuLyLine3 = xu_ly_anh(frame, array_1, Npixel)
        a0_2,b0_2,c0_2,d0_2, time_xuLyLine4 = xu_ly_anh(frame, array_2, Npixel)
        
        values_y = c0
        values_y_0 = c0_0
        values_y_1 = c0_1
        values_y_2 = c0_2
        row = 100
        threshold_code = [0,1,1,1,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0]
        input_var = 16

        # a00, a1, a2, a3, a4, a5, a6, a7, a8, a9 = xly.xu_ly_y(array2, values_y, row, threshold_code, input_var)
        # a00_0, a1_0, a2_0, a3_0, a4_0, a5_0, a6_0, a7_0, a8_0, a9_0 = xly.xu_ly_y(array2, values_y_0, row, threshold_code, input_var)
        a00, a1, a2, a3, a9, time_xuLy_y1 = xu_ly_y(array2, values_y, row, threshold_code, input_var)
        a00_0, a1_0, a2_0, a3_0, a9_0, time_xuLy_y2= xu_ly_y(array2, values_y_0, row, threshold_code, input_var)
        a00_1, a1_1, a2_1, a3_1, a9_1, time_xuLy_y3 = xu_ly_y(array2, values_y_1, row, threshold_code, input_var)
        a00_2, a1_2, a2_2, a3_2, a9_2, time_xuLy_y4 = xu_ly_y(array2, values_y_2, row, threshold_code, input_var)

        # print("sac xuat1:", a6)
        # print("sac xuat2:", a6_0)
        
    #        print("so lan xuat hien:", a7)
        print("data 1", a9)
        print("data 2", a9_0)
        print("data 3", a9_1)
        print("data 4", a9_2)
    #        print("so hang lay duoc: ", a9)    #        cv2.imshow('frame', img)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        frame2 = cv2.resize(frame2,(780,550))
        # height, width, channels = frame2.shape
        # print(f"height, width:{height, width}")
        font = cv2.FONT_HERSHEY_SIMPLEX
        end_time_total = time.time()
        total_time_00 = end_time_total - start_time_total

        total_time_01 = time_checkRoI + time_veRoi1 + time_veRoi2 + time_veRoi3 + time_veRoi4 + time_xuLyLine1 + time_xuLyLine2 +time_xuLyLine3 + time_xuLyLine4 + time_xuLy_y1 + time_xuLy_y2 + time_xuLy_y3 + time_xuLy_y4

        # print("total_time:", total_time_00)

        
        cv2.imshow("Frame2", frame2)
        # if cv2.waitKey(1) & 0xFF == ord('p'):
        #     cv2.waitKey(-1) 

    # vid.release()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return a9, a9_0, a9_1, a9_2
    # return a9

def check_roi_tu_arr(str_x, Y, top, bot, Npixel):
    start_time1 = time.time()
    j = 1
    k = 0
    str_out1 = np.zeros((60, 4), dtype = int)
    str_out2 = np.zeros((60, 4), dtype = int) 
    str_out3 = np.zeros((60, 4), dtype = int)
    str_out4 = np.zeros((60, 4), dtype = int) 

    str_out5 = np.zeros((60, 4), dtype = int)
    str_out6 = np.zeros((60, 4), dtype = int)
    str_out7 = np.zeros((60, 4), dtype = int)
    str_out8 = np.zeros((60, 4), dtype = int)

    n = len(str_x)

    max1 = str_x[0]
    min1 = str_x[0]

    str_out1[0][0] = str_x[0]
    str_out1[0][1] = Y[0]
    str_out1[0][2] = top[0]
    str_out1[0][3] = bot[0]

    for i in range(1,n):
        if abs(str_x[i] - max1) <= 0.2 * max1 or abs(str_x[i] - min1) <= 0.2 * min1:
            str_out1[j][0] = str_x[i] 
            str_out1[j][1] = Y[i]
            str_out1[j][2] = top[i]
            str_out1[j][3] = bot[i]
            j = j + 1;

            if str_x[i] > max1:
                max1 = str_x[i]
            if str_x[i] < min1:
                min1 = str_x[i]

        else:
            str_out2[k][0] = str_x[i]
            str_out2[k][1] = Y[i]
            str_out2[k][2] = top[i]
            str_out2[k][3] = bot[i]
            k = k + 1

    max2 = str_out2[0][0]
    min2 = str_out2[0][0]
    str_out3[0][0] = str_out2[0][0]
    str_out3[0][1] = str_out2[0][1]
    str_out3[0][2] = str_out2[0][2]
    str_out3[0][3] = str_out2[0][3]

    j2 = 1
    k2 = 0

    for i2 in range(1, np.size(str_out2,0)): 
        if abs(str_out2[i2][0] - max2) <= 0.2 * max2 or abs(str_out2[i2][0] - min2) <= 0.2 * min2:
            str_out3[j2][0] = str_out2[i2][0]
            str_out3[j2][1] = str_out2[i2][1]
            str_out3[j2][2] = str_out2[i2][2]
            str_out3[j2][3] = str_out2[i2][3]
            j2 = j2 + 1
            if str_out2[i2][0] > max2:
                max2 = str_out2[i2][0]
            if str_out2[i2][0] < min2:
                min2 = str_out2[i2][0]
        else:
            str_out4[k2][0] = str_out2[i2][0]
            str_out4[k2][1] = str_out2[i2][1]
            str_out4[k2][2] = str_out2[i2][2]
            str_out4[k2][3] = str_out2[i2][3]
            k2 = k2 + 1
    
    max3 = str_out4[0][0]
    min3 = str_out4[0][0]
    str_out5[0][0] = str_out4[0][0]
    str_out5[0][1] = str_out4[0][1]
    str_out5[0][2] = str_out4[0][2]
    str_out5[0][3] = str_out4[0][3]

    j3 = 1
    k3 = 0

    for i3 in range(1, np.size(str_out4,0)):
        if abs(str_out4[i3][0] - max3) <= 0.2 * max3 or abs(str_out4[i3][0] - min3) <= 0.2 * min3:
            str_out5[j3][0] = str_out4[i3][0]
            str_out5[j3][1] = str_out4[i3][1]
            str_out5[j3][2] = str_out4[i3][2]
            str_out5[j3][3] = str_out4[i3][3]
            j3 = j3 + 1
            if str_out4[i3][0] > max3:
                max3 = str_out4[i3][0]
            if str_out4[i3][0] < min3:
                min3 = str_out4[i3][0]
        else:
            str_out6[k3][0] = str_out4[i3][0]
            str_out6[k3][1] = str_out4[i3][1]
            str_out6[k3][2] = str_out4[i3][2]
            str_out6[k3][3] = str_out4[i3][3]
            k3 = k3 + 1

    max4 = str_out6[0][0]
    min4 = str_out6[0][0]
    str_out7[0][0] = str_out6[0][0]
    str_out7[0][1] = str_out6[0][1]
    str_out7[0][2] = str_out6[0][2]
    str_out7[0][3] = str_out6[0][3]

    j4 = 1
    k4 = 0

    for i4 in range(1, np.size(str_out6,0)):
        if abs(str_out6[i4][0] - max4) <= 0.2 * max4 or abs(str_out6[i4][0] - min4) <= 0.2 * min4:
            str_out7[j4][0] = str_out6[i4][0]
            str_out7[j4][1] = str_out6[i4][1]
            str_out7[j4][2] = str_out6[i4][2]
            str_out7[j4][3] = str_out6[i4][3]
            j4 = j4 + 1
            if str_out6[i4][0] > max4:
                max4 = str_out6[i4][0]
            if str_out6[i4][0] < min4:
                min4 = str_out6[i4][0]
        else:
            str_out8[k4][0] = str_out6[i4][0]
            str_out8[k4][1] = str_out6[i4][1]
            str_out8[k4][2] = str_out6[i4][2]
            str_out8[k4][3] = str_out6[i4][3]
            k4 = k4 + 1

    in1 = str_out1
    in2 = str_out3
    in3 = str_out5
    in4 = str_out7
    str_ = np.zeros(4, dtype = int)
    str_2 = np.zeros(4, dtype = int)
    str_outout1 = np.zeros(4, dtype = int)
    str_outout2 = np.zeros(4, dtype = int)
    str_outout3 = np.zeros(4, dtype = int)
    str_outout4 = np.zeros(4, dtype = int)
                    
    n = 60
    i1 = i2 = i3 = i4 = 0
    j1 = j2 = j3 = j4 = 0
    tg = 0
    a = b = c = 0
    max1 = max2 = max3 = max4 = 0
    x_top = x_bot = 0
    x_top2 = x_bot2 = 0
    x_top3 = x_bot3 = 0
    x_top4 = x_bot4 = 0
    min1 = min2 = min3 = min4 = 0


    for i1 in range(0, 60):
        if in1[i1][0] != 0 and in1[i1][1] != 0:
            j1 = j1 + 1
        if in2[i1][0] != 0 and in2[i1][1] != 0:
            j2 = j2 + 1
        if in3[i1][0] != 0 and in3[i1][1] != 0:
            j3 = j3 + 1
        if in4[i1][0] != 0 and in4[i1][1] != 0:
            j4 = j4 + 1
    str_[0] = j1;
    str_[1] = j2;
    str_[2] = j3;
    str_[3] = j4;

    for a in range(0, 3):
        for b in range(a+1, 4):
            if str_[a] < str_[b]:
                tg = str_[a]
                str_[a] = str_[b]
                str_[b] = tg
    for i in range(0,4):
        print(f"sort{i}:{str_[i]}")

    print(f"sap xep contours j1,j2,j3,j4:{j1}, {j2}, {j3}, {j4}")
    # truong hop co 1 den
    if str_[0] == j1:
        max1 = 0
        min1 = in1[0][3]
        for i2 in range(0, j1):
            if in1[i2][2] > max1:
                max1 = in1[i2][2]
                x_top = in1[i2][0]
            if in1[i2][3] <= min1:
                min1 = in1[i2][3]
                x_bot = in1[i2][0]
        print(f"xtop:{x_top} and xbot:{x_bot} of j1 led1")
        str_outout1[0] = (x_top + x_bot)/2
        str_outout1[1] = min1
        str_outout1[2] = (x_top + x_bot)/2
        str_outout1[3] = max1
    
    elif str_[0] == j2 and j2 != j1:
        max1 = 0
        min1 = in2[0][3]
        for i2 in range(0, j2):
            if in2[i2][2] > max1:
                max1 = in2[i2][2]
                x_top = in2[i2][0]
            if in2[i2][3] <= min1:
                min1 = in2[i2][3]
                x_bot = in2[i2][0]
        print(f"xtop:{x_top} and xbot:{x_bot} of j2 led1")
        str_outout1[0] = (x_top + x_bot)/2
        str_outout1[1] = min1
        str_outout1[2] = (x_top + x_bot)/2
        str_outout1[3] = max1
        
    elif str_[0] == j3 and (j3 != j1 or j3 != j2) :
        max1 = 0
        min1 = in3[0][3]
        for i2 in range(0, j3):
            if in3[i2][2] > max1:
                max1 = in3[i2][2]
                x_top = in3[i2][0]
            if in3[i2][3] <= min1:
                min1 = in3[i2][3]
                x_bot = in3[i2][0]
        print(f"xtop:{x_top} and xbot:{x_bot} of j3 led1 ")
        str_outout1[0] = (x_top + x_bot)/2
        str_outout1[1] = min1
        str_outout1[2] = (x_top + x_bot)/2
        str_outout1[3] = max1

    elif str_[0] == j4 and (j4 != j1 or j4 != j2 or j4 != j3 ):
        max1 = 0
        min1 = in4[0][3]
        for i2 in range(0, j4):
            if in4[i2][2] > max1:
                max1 = in4[i2][2]
                x_top = in4[i2][0]
            if in4[i2][3] <= min1:
                min1 = in4[i2][3]
                x_bot = in4[i2][0]
        print(f"xtop:{x_top} and xbot:{x_bot} of j4 led1")
        str_outout1[0] = (x_top + x_bot)/2
        str_outout1[1] = min1
        str_outout1[2] = (x_top + x_bot)/2
        str_outout1[3] = max1

    # truong hop co den so 2
    gocLech = goc_lech.degrees(goc_lech.atan2(abs(x_top - x_bot),abs(max1 - min1)))
    print(f"goc lech RoI:{gocLech}")
    # if abs(max1 - min1) >= 50*Npixel and gocLech <= 2 and max1 > 0:
    #     str_outout1[0] = (x_top + x_bot)/2
    #     str_outout1[1] = min1
    #     str_outout1[2] = (x_top + x_bot)/2
    #     str_outout1[3] = min1 + 20*Npixel

    #     str_outout3[0] = (x_top + x_bot)/2
    #     str_outout3[1] = max1 - 20*Npixel
    #     # str_outout3[1] = max1 
    #     str_outout3[2] = (x_top + x_bot)/2
    #     str_outout3[3] = max1
    # if abs(max1 - min1) >= 75*Npixel:
        # pass
        # str_outout2[0] = (x_top + x_bot)/2
        # str_outout2[1] = max1 - 24*Npixel
        # str_outout2[2] = (x_top + x_bot)/2
        # str_outout2[3] = max1

        # str_outout1[0] = (x_top + x_bot)/2
        # str_outout1[1] = min1
        # str_outout1[2] = (x_top + x_bot)/2
        # str_outout1[3] = min1 + 50*Npixel
    
    # elif abs(max1 - min1) >= 50*Npixel and gocLech > 2 and max1 > 0:
    #     str_outout1[0] = x_bot
    #     str_outout1[1] = min1
    #     str_outout1[2] = x_bot
    #     str_outout1[3] = min1 + 20*Npixel

    #     str_outout3[0] = x_top
    #     str_outout3[1] = max1 - 20*Npixel
    #     str_outout3[2] = x_top
    #     str_outout3[3] = max1


    # else:
    #     str_outout1[0] = (x_top + x_bot)/2
    #     str_outout1[1] = min1 - 2*Npixel
    #     str_outout1[2] = (x_top + x_bot)/2
    #     str_outout1[3] = max1 + 2*Npixel    

    # else:
    if str_[1] == j1 and j1 < str_[0]:
        max2 = 0
        min2 = in1[0][3]
        for i3 in range(0, j1):
            if in1[i3][2] > max2:
                max2 = in1[i3][2]
                x_top2 = in1[i3][0]
            if in1[i3][3] <= min2:
                min2 = in1[i3][3]
                x_bot2 = in1[i3][0]
        print(f"xtop:{x_top2} and xbot:{x_bot2} of j1 led2")
        str_outout2[0] = (x_top2 + x_bot2)/2
        str_outout2[1] = min2
        str_outout2[2] = (x_top2 + x_bot2)/2
        str_outout2[3] = max2
        print(f"str_outout2[1] == j1: {str_outout2[:]}")
    
    elif str_[1] == j2 and ((j2 != j1 and j2 < str_[0]) or (j2 == j1 == str_[0])) :
        max2 = 0
        min2 = in2[0][3]
        for i3 in range(0, j2):
            if in2[i3][2] > max2:
                max2 = in2[i3][2]
                x_top2 = in2[i3][0]
            if in2[i3][3] <= min2:
                min2 = in2[i3][3]
                x_bot2 = in2[i3][0]
        print(f"xtop:{x_top2} and xbot:{x_bot2} of j2 led2")
        str_outout2[0] = (x_top2 + x_bot2)/2
        str_outout2[1] = min2
        str_outout2[2] = (x_top2 + x_bot2)/2
        str_outout2[3] = max2
        print(f"str_outout2[1] == j2: {str_outout2[:]}")

    elif str_[1] == j3 and ((j3 == j2 == str_[0]) or (j3 == j1 == str_[0]) or (j3 != j2 and j3 !=j1 and j3 < str_[0])):
        max2 = 0
        min2 = in3[0][3]
        for i3 in range(0, j3):
            if in3[i3][2] > max2:
                max2 = in3[i3][2]
                x_top2 = in3[i3][0]
            if in3[i3][3] <= min2:
                min2 = in3[i3][3]
                x_bot2 = in3[i3][0]
        print(f"xtop:{x_top2} and xbot:{x_bot2} of j3 led2")
        str_outout2[0] = (x_top2 + x_bot2)/2
        str_outout2[1] = min2
        str_outout2[2] = (x_top2 + x_bot2)/2
        str_outout2[3] = max2
        print(f"str_outout2[1] == j3: {str_outout2[:]}")

    elif str_[1] == j4 and ((j4 == j3 == str_[0]) or (j4 == j2 == str_[0]) or (j4 == j1 == str_[0]) or (j4 != j2 and j4 != j1 and j4 < str_[0]) or (j4 != j3 and j4 != j1 and j4 < str_[0]) or (j4 != j2 and j4 != j3 and j4 < str_[0])):
        max2 = 0
        min2 = in4[0][3]
        for i3 in range(0, j4):
            if in4[i3][2] > max2:
                max2 = in4[i3][2]
                x_top2 = in4[i3][0]
            if in4[i3][3] <= min2:
                min2 = in4[i3][3]
                x_bot2 = in4[i3][0]
        
        print(f"xtop:{x_top2} and xbot:{x_bot2} of j4 led2")
        str_outout2[0] = (x_top2 + x_bot2)/2
        str_outout2[1] = min2
        str_outout2[2] = (x_top2 + x_bot2)/2
        str_outout2[3] = max2
        print(f"str_outout2[1] == j4: {str_outout2[:]}")
    
    gocLech = goc_lech.degrees(goc_lech.atan2(abs(x_top2 - x_bot2),abs(max2 - min2)))
    print(f"goc lech RoI:{gocLech}")
    if abs(max2 - min2) >= 50*Npixel and gocLech <= 2 and max2 > 0 :
        str_outout2[0] = (x_top2 + x_bot2)/2
        str_outout2[1] = min2
        str_outout2[2] = (x_top2 + x_bot2)/2
        str_outout2[3] = min2 + 20*Npixel

        str_outout4[0] = (x_top2 + x_bot2)/2
        str_outout4[1] = max2 - 20*Npixel
        str_outout4[2] = (x_top2 + x_bot2)/2
        str_outout4[3] = max2
    
    elif abs(max2 - min2) >= 50*Npixel and gocLech > 2 and max2 > 0 :
        str_outout2[0] = x_bot2
        str_outout2[1] = min2
        str_outout2[2] = x_bot2
        str_outout2[3] = min2 + 20*Npixel


        str_outout4[0] = x_top2
        str_outout4[1] = max2 - 20*Npixel
        str_outout4[2] = x_top2
        str_outout4[3] = max2
        

    print(f"str_outout2 in 2 RoI:{str_outout2}")
    # 3 RoI khac nhau
    if str_[2] == j1 and (j1 < str_[1]) and str_[2] > 0:
        max3 = 0
        min3 = in1[0][3]
        for i3 in range(0, j1):
            if in1[i3][2] > max3:
                max3 = in1[i3][2]
                x_top3 = in1[i3][0]
            if in1[i3][3] <= min3:
                min3 = in1[i3][3]
                x_bot3 = in1[i3][0]
        print(f"xtop:{x_top3} and xbot:{x_bot3} of j1 led3")
        str_outout4[0] = (x_top3 + x_bot3)/2
        str_outout4[1] = min3
        str_outout4[2] = (x_top3 + x_bot3)/2
        str_outout4[3] = max3
        print(f"str_outout4[2] == j1: {str_outout4[:]}")

    elif str_[2] == j2 and ((j1 == j2 == str_[1]) or (j2 != j1 and j2 < str_[1])) and str_[2] > 0 :
        max3 = 0
        min3 = in2[0][3]
        for i3 in range(0, j2):
            if in2[i3][2] > max3:
                max3 = in2[i3][2]
                x_top3 = in2[i3][0]
            if in2[i3][3] <= min3:
                min3 = in2[i3][3]
                x_bot3 = in2[i3][0]
        print(f"xtop:{x_top3} and xbot:{x_bot3} of j2 led3")
        str_outout4[0] = (x_top3 + x_bot3)/2
        str_outout4[1] = min3
        str_outout4[2] = (x_top3 + x_bot3)/2
        str_outout4[3] = max3
        print(f"str_outout4[2] == j2: {str_outout4[:]}")

    
    elif str_[2] == j3 and ((j3 == j2 == str_[1]) or (j3 == j1 == str_[1]) or (j3 != j2 and j3 != j1 and j3 < str_[1])) and str_[2] > 0:
        max3 = 0
        min3 = in3[0][3]
        for i3 in range(0, j3):
            if in3[i3][2] > max3:
                max3 = in3[i3][2]
                x_top3 = in3[i3][0]
            if in3[i3][3] <= min3:
                min3 = in3[i3][3]
                x_bot3 = in3[i3][0]
        print(f"xtop:{x_top3} and xbot:{x_bot3} of j3 led3")
        str_outout4[0] = (x_top3 + x_bot3)/2
        str_outout4[1] = min3
        str_outout4[2] = (x_top3 + x_bot3)/2
        str_outout4[3] = max3
        print(f"str_outout4[2] == j3: {str_outout4[:]}")

    elif str_[2] == j4 and ((j4 == j3 == str_[1]) or (j4 == j2 == str_[1]) or (j4 == j1 == str_[1]) or (j4 != j1 and j4 < str_[1]) or (j4 != j2 and j4 < str_[1]) or (j4 != j3 and j4 < str_[1])) and str_[2] > 0 :
        max3 = 0
        min3 = in4[0][3]
        for i3 in range(0, j4):
            if in4[i3][2] > max3:
                max3 = in4[i3][2]
                x_top3 = in4[i3][0]
            if in4[i3][3] <= min3:
                min3 = in4[i3][3]
                x_bot3 = in4[i3][0]
        print(f"xtop:{x_top3} and xbot:{x_bot3} of j4 led3")
        str_outout4[0] = (x_top3 + x_bot3)/2
        str_outout4[1] = min3
        str_outout4[2] = (x_top3 + x_bot3)/2
        str_outout4[3] = max3
        print(f"str_outout4[2] == j4: {str_outout4[:]}")
    
    gocLech = goc_lech.degrees(goc_lech.atan2(abs(x_top3 - x_bot3),abs(max3 - min3)))
    # print(f"goc lech RoI:{gocLech}")
    if abs(max3 - min3) >= 50*Npixel and gocLech <= 2 and max3 > 0:
        str_outout2[0] = (x_top3 + x_bot3)/2
        str_outout2[1] = min3
        str_outout2[2] = (x_top3 + x_bot3)/2
        str_outout2[3] = min3 + 20*Npixel

        str_outout4[0] = (x_top3 + x_bot3)/2
        str_outout4[1] = max3 - 20*Npixel
        str_outout4[2] = (x_top3 + x_bot3)/2
        str_outout4[3] = max3
    
    elif abs(max3 - min3) >= 50*Npixel and gocLech > 2 and max3 > 0 :
        str_outout2[0] = x_bot3
        str_outout2[1] = min3
        str_outout2[2] = x_bot3
        str_outout2[3] = min3 + 20*Npixel


        str_outout4[0] = x_top3
        str_outout4[1] = max3 - 20*Npixel
        str_outout4[2] = x_top3
        str_outout4[3] = max3

    print(f"toa do RoI4 ham 3 RoI: {str_outout4[:]}")
    print(f"str_outout2 in 3 RoI:{str_outout2}")


    # 4 RoI khac nhau
    if str_[3] == j1  and (j1 < str_[2]) and str_[3] > 0:
        max4 = 0
        min4 = in1[0][3]
        for i3 in range(0, j1):
            if in1[i3][2] > max4:
                max4 = in1[i3][2]
                x_top4 = in1[i3][0]
            if in1[i3][3] <= min4:
                min4 = in1[i3][3]
                x_bot4 = in1[i3][0]
        print(f"xtop:{x_top4} and xbot:{x_bot4} of j1 led4")
        str_outout4[0] = (x_top4 + x_bot4)/2
        str_outout4[1] = min4
        str_outout4[2] = (x_top4 + x_bot4)/2
        str_outout4[3] = max4
        print(f"str_outout4[3] == j1: {str_outout4[:]}")

    elif str_[3] == j2 and ((j2 == j1 == str_[2]) or (j2 != j1 and j2 < str_[2]) and j2 < str_[1]) and str_[3] > 0 :
        max4 = 0
        min4 = in2[0][3]
        for i3 in range(0, j2):
            if in2[i3][2] > max4:
                max4 = in2[i3][2]
                x_top4 = in2[i3][0]
            if in2[i3][3] <= min4:
                min4 = in2[i3][3]
                x_bot4 = in2[i3][0]
        print(f"xtop:{x_top4} and xbot:{x_bot4} of j2 led4")
        str_outout4[0] = (x_top4 + x_bot4)/2
        str_outout4[1] = min4
        str_outout4[2] = (x_top4 + x_bot4)/2
        str_outout4[3] = max4
        print(f"str_outout4[3] == j2: {str_outout4[:]}")

    elif str_[3] == j3 and ((j3 == j2 == str_[2]) or (j3 == j1 == str_[2]) or (j3 != j2 and j3 != j1 and j3 < str_[2])) and str_[3] > 0:
        max4 = 0
        min4 = in3[0][3]
        for i3 in range(0, j3):
            if in3[i3][2] > max4:
                max4 = in3[i3][2]
                x_top4 = in3[i3][0]
            if in3[i3][3] <= min4:
                min4 = in3[i3][3]
                x_bot4 = in3[i3][0]
        print(f"xtop:{x_top4} and xbot:{x_bot4} of j3 led4")
        str_outout4[0] = (x_top4 + x_bot4)/2
        str_outout4[1] = min4
        str_outout4[2] = (x_top4 + x_bot4)/2
        str_outout4[3] = max4
        print(f"str_outout4[3] == j3: {str_outout4[:]}")

    elif str_[3] == j4 and ((j4 == j3 == str_[2]) or (j4 == j2 == str_[2]) or (j4 == j1 == str_[2]) or (j4 < str_[2])) and str_[3] > 0:
        max4 = 0
        min4 = in4[0][3]
        for i3 in range(0, j4):
            if in4[i3][2] > max4:
                max4 = in4[i3][2]
                x_top4 = in4[i3][0]
            if in4[i3][3] <= min4:
                min4 = in4[i3][3]
                x_bot4 = in4[i3][0]
        print(f"xtop:{x_top4} and xbot:{x_bot4} of j4 led4")
        str_outout4[0] = (x_top4 + x_bot4)/2
        str_outout4[1] = min4
        str_outout4[2] = (x_top4 + x_bot4)/2
        str_outout4[3] = max4
        print(f"str_outout4[3] == j4: {str_outout4[:]}")
    
    gocLech = goc_lech.degrees(goc_lech.atan2(abs(x_top4 - x_bot4),abs(max4 - min4)))
    # print(f"goc lech RoI:{gocLech}")
    # if abs(max4 - min4) >= 50*Npixel and gocLech <= 2 and max4 > 0 :
    #     str_outout4[0] = (x_top4 + x_bot4)/2
    #     str_outout4[1] = min4
    #     str_outout4[2] = (x_top4 + x_bot4)/2
    #     str_outout4[3] = min4 + 20*Npixel

    #     str_outout4[0] = (x_top4 + x_bot4)/2
    #     str_outout4[1] = max4 - 20*Npixel
    #     str_outout4[2] = (x_top4 + x_bot4)/2
    #     str_outout4[3] = max4
    
    # elif abs(max4 - min4) >= 50*Npixel and gocLech > 2 and max4 > 0 :
    #     str_outout4[0] = x_bot4
    #     str_outout4[1] = min4
    #     str_outout4[2] = x_bot4
    #     str_outout4[3] = min4 + 20*Npixel


    #     str_outout4[0] = x_top4
    #     str_outout4[1] = max4 - 20*Npixel
    #     str_outout4[2] = x_top4
    #     str_outout4[3] = max4
    print(f"str_outout2 in 4 RoI:{str_outout2}")
    print(f"toa do RoI4 ham 4 RoI: {str_outout4[:]}")

    end_time1 = time.time()
    total_time1 =end_time1 - start_time1
    return str_outout1, str_outout2, str_outout3, str_outout4, total_time1

def ve_roi(img, text, array, x):
    start_time2 = time.time()
    x1 = array[0]
    x2 = array[1]
    x3 = array[2]
    x4 = array[3]

    y1 = 0
    y2 = x4

    if x3 + 10 > x:
        y1 = x3 - 15
    else:
        y1 = 5 + x3

    img = cv2.line(img,(x1,x2),(x3,x4),(0,0,255),1,cv2.LINE_AA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.putText(img, text, (y1,y2), font, 1.5, (0,0,255),2,cv2.LINE_AA)

    end_time2 = time.time()
    total_time2 =  end_time2 - start_time2
    return img, total_time2

def xu_ly_anh(img, array, Npixel):
    start_time3 = time.time()

    x1 = array[0] #ok fix 480
    y1 = array[1]
    x2 = array[2]
    y2 = array[3]
    # print(f"array:{array[:]}")
    i=0
    Pixels_Line = [] # sua duoc loi pixel line la bien public
    

    if y2 - y1 <0:
        Pixels_Line = np.zeros((y1-y2+1),dtype = int)
    
        for y in range(y1, y2-1,-1):
            Pixels_Line[i] = img[y,x1]
            i = i + 1

    if y2 - y1 >0:
        Pixels_Line = np.zeros((y2-y1+1),dtype = int)
        for y in range(y1, y2+1,+1):
            Pixels_Line[i] = img[y,x1] # sua dung pixel 480 and 50
            i = i + 1

    # print(f"gia tri pixel:{Pixels_Line[:]}")        

    N = len(Pixels_Line) 
    # x_list = [int(i) for i in range(N)]
    # Mang_input_waveform = np.zeros(N,dtype = float)

    # for i in range(0,N):
    #     Mang_input_waveform[i] = i/Npixel


    # print(f"len(Pixel_Line): {N}")
    # array_final = np.zeros(abs(y1-y2)+10, dtype = int)
    # i = j = k = 0
    # for k in range(0, N):
    #     array_final[k] = -1
    # for i in range(0, N):
    #     if i%Npixel == 0:
    #         array_final[j] = Pixels_Line[i]
    #         j = j + 1

    npixel_final = int(N/Npixel + 10)
    array_final = np.zeros(npixel_final, dtype = int)
    i = j = k = 0
    for k in range(0, npixel_final):
        array_final[k] = -1
    for i in range(0, N, Npixel):
        if i%Npixel == 0:
            array_final[j] = Pixels_Line[i]
            j = j + 1

    end_time3 = time.time()
    total_time3 = end_time3 - start_time3
    # print(f"gia tri pixel:{array_final[:]}")
    # return N, Pixels_Line, array_final, N, Mang_input_waveform, x_list
    return N, Pixels_Line, array_final, N, total_time3

def xu_ly_y(array2, values_y, row, threshold_code, input_var):

    start_time4 = time.time()
# values_x = [int(i) for i in range(len(values_y))]  # nếu không dùng để show curve fit mapping vì không hỗ trợ kiểu List, phải chuyển sang kiểu array
    values_x = np.zeros(len(values_y), dtype=int)        # dùng khi show curve fit mapping 
    for k in range(0, len(values_y)):
        values_x[k] = k

    # print(f"type of value_x: {type(values_x)}")
    mse_y_values = [int(i) for i in range(len(values_y))] 
    # print(f"value y: {values_y[:]}")
    def mapping1(values_x, a0, a1, a2, a3):
        return a3 * values_x**3 + a2 * values_x**2 + a1 * values_x + a0

    args, _ = curve_fit(mapping1, values_x, values_y)

    # print(f"args: {args}")
    # a_opt, b_opt, c_opt, d_opt = args
    # y_model = mapping1(values_x, a_opt, b_opt, c_opt, d_opt)
    # plt.scatter(values_x, values_y)
    # plt.plot(values_x, y_model, color = 'r')
    # plt.plot(values_x, values_y, color = 'blue')
    # plt.show()  
    mse_final = 0
    for i in range(0,len(values_y)):
        mse_y = args[0] + args[1]*i + args[2]*i**2 + args[3] * i**3
        mse = ((values_y[i] - mse_y)**2)/len(values_y)
        mse_final += mse 
        mse_y_values[i] = mse_y 
    # print(f"mse_y: {mse_y_values}")
    
    mang_so_sanh = [int(i) for i in range(len(values_y))] 
    so_sanh = 0
    for i in range(0,len(values_y)):
        if values_y[i] >= mse_y_values[i]:
            so_sanh = 1
        else:
            so_sanh = 0
        mang_so_sanh[i] = so_sanh

    print(f"values of mang so sanh: {mang_so_sanh[:]}")
    # if len(mang_so_sanh) >= len(array2[0]):
    #     c = np.pad(array2, [(0, 0),(0, len(mang_so_sanh) - len(array2[0]))], mode='constant')
    #     array_append = np.append([mang_so_sanh],c,axis=0)
    # else:
    #     c = np.pad(mang_so_sanh, (0, len(array2[0]) - len(mang_so_sanh)), 'constant')
    #     array_append = np.append([c],array2,axis=0)

    # so_hang_lay_duoc = len(array_append[0])
    # if so_hang_lay_duoc <= row:
    #     subarray = array_append
    # else:
    #     subarray = array_append[0:row]

    # a_man = []

    # for i in range(0, len(threshold_code)):
    #     if threshold_code[i] == 1:
    #         a_man = np.append(a_man, [0,1])
    #     else:
    #         a_man = np.append(a_man, [1,0])
    # a_man = list(map(int, a_man))
    # so_mau = len(subarray)*len(subarray[0])

    # n = len(values_y)
    # s = 0
    # for i in range(n):
    #     s = s + values_y[i]
    # threshold = s/n

    # mang_2d_dau_vao = subarray
    # if np.size(mang_2d_dau_vao,0) < row: 
    #     n_loop = np.size(mang_2d_dau_vao,0)
    # else:
    #     n_loop = row

    mang_2d_dau_vao = mang_so_sanh
    n_loop = 1

    # c = np.size(mang_2d_dau_vao,1)  
    c = np.size(mang_2d_dau_vao)  # hàm trả về số cột của mang_2d_dau_vao and = 500
    d = np.size(threshold_code)
    b = threshold_code
    # MANG = np.zeros((n_loop,20), dtype = int) 
    # MANG_index = np.zeros((n_loop,20), dtype = int)
    # MANG_test = np.zeros((n_loop,20), dtype = int)
    # MANG_heso = np.zeros((n_loop,20), dtype = int)
    # MANG_daura = np.zeros(n_loop, dtype = int)

    MANG = np.zeros(20, dtype = int) #  column = 20
    MANG_index = np.zeros(20, dtype = int)
    MANG_test = np.zeros(20, dtype = int)
    MANG_heso = np.zeros(20, dtype = int)
    MANG_daura = np.zeros(n_loop, dtype = int) # sô phần tử = n_loop

    i = j = k = m = n = o = 0
    x = np.zeros(20, dtype = int) 
    heso = np.zeros(20, dtype = int)
    test = np.zeros(20, dtype = int)
    index = np.zeros(20, dtype = int)
    kiemtra = np.zeros(20, dtype = int)
    count = countdem = max1 = 0
    sizeb = 20
    max1_3 = 0
    value = -1
    size = sizeb 

    # for i_loop in range(0, n_loop): # vong lap lon nhat
    # a = mang_2d_dau_vao[i_loop]
    a = mang_2d_dau_vao
    i = 0
    n = 0
    for k in range(0,20):
        x[k] = -1
    print(f"c-d+1: {c-d+1}")
    for j in range(0, c-d+1):
        for m in range(0, d-input_var):
            n = n + abs(a[j+m] - b[m])
        if n == 0:
            for o in range(0, input_var):
                # print("i,j,d,o, trong1, trong2", i,j,d,o, i+o, j+d-input_var+o)
                if i + o < 20:  #ok fix xong 20. ctr chạy êm ru.
                    x[i + o] = a[j+d-input_var+o]
                else:
                    pass

            i = i + input_var
        n = 0

    # MANG[i_loop] = x
    MANG = x
    print("gia tri mang x:",x)
    for k2 in range(0, sizeb):
        heso[k2] = -1
        kiemtra[k2] = -1
    for i2 in range(0, sizeb - input_var, 4):
        if x[i2] == -1: 
            break
        else:
            heso[int(i2/2)] = 0
            for j2 in range (0, input_var):
                heso[int(i2/2)] = heso[int(i2/2)] + x[i2+j2]*(1 << j2)
                kiemtra[i2] = 1 << j2
    # print("gia tri thap phan cua mang:",heso)
    for l2 in range(0, 20):
        test[l2] = -1
        index[l2] = -1
    max1 = 0
    countdem = 0
    for m2 in range(0,20): 
        count = 0
        countdem = 0
        for n2 in range(0, 20):
            if heso[m2] == test[n2]:
                count = 1
        if count != 1:
            for o2 in range(0, 20):
                if heso[m2] == heso[o2]:
                    countdem = countdem + 1
            index[max1] = countdem
            test[max1] = heso[m2]
            max1 = max1 + 1
    
    # MANG_index[i_loop] = index
    # MANG_test[i_loop]  = test
    # MANG_heso[i_loop]  = heso

        
    MANG_index = index
    MANG_test = test
    MANG_heso  = heso

    max1_3 = 0
    value3 = -1
    for i3 in range(0, size):
        if index[i3] > max1_3:
            max1_3 = index[i3]
            value3 = test[i3]
    daura = value3
    # MANG_daura[i_loop] = daura 
    MANG_daura = daura 

    array = [input_var]*n_loop
    size4 = np.size(MANG_daura)

    test4 = np.zeros(20, dtype = int)
    index4 = np.zeros(20, dtype = int)

    count4 = countdem4 = max1_4 = max2_4 = daura4 = value4 = 0
    max3_4 = maxfinal = index3_4 = indexfinal = 0

    for l4 in range(0,20):
        test4[l4] = -1
        index4[l4] = -1

    max1_4 = 0
    countdem4 = 0
    # size4 = len(MANG_daura)
    size4 = 1

    # for m4 in range(0, size4):
    count4 = 0
    countdem4 = 0
    for n4 in range(0, 20):
        # if MANG_daura[m4] == test4[n4] or MANG_daura[m4] == -1:
        if MANG_daura == test4[n4] or MANG_daura == -1:
            count4 = 1
    if count4 != 1:
        # for o4 in range(0,size4):
        # if MANG_daura[m4] == MANG_daura[o4]:
        #     countdem4 = countdem4 + 1
        # index4[max1_4] = countdem4
        # test4[max1_4] = MANG_daura[m4]
        # max1_4 = max1_4 + 1

        if MANG_daura == MANG_daura:
            countdem4 = countdem4 + 1
        index4[max1_4] = countdem4
        test4[max1_4] = MANG_daura
        max1_4 = max1_4 + 1

    max2_4 = 0
    value4 = -1
    for i4 in range(0, 20):
        if index4[i4] > max2_4:
            max3_4 = max2_4
            index3_4 = value4
            max2_4 = index4[i4]
            value4 = test4[i4]
    if value4 != -1:
        daura4 = 100*max2_4/size4
        indexfinal = value4
        maxfinal = max2_4
    else:
        daura4 = 100*max3_4/size4
        indexfinal = index3_4
        maxfinal = max3_4 

    
    digit =  4
    def twosCom_decBin(dec, digit):
        bin1 = ""
        if dec>=0:
            bin1 = bin(dec).split("0b")[1]
            while len(bin1)<digit :
                bin1 = '0'+bin1
            return bin1
        else:
            bin1 = -1*dec
            return bin(bin1-pow(2,digit)).split("0b")[1]
    print("value4:", value4)
    bin1 = twosCom_decBin(value4, 32) 
    bin1 = str(bin1)[::-1] 
    bin1 = [int(i) for i in str(bin1)] 
    bin1 = bin1[0:digit]

    end_time4 = time.time()
    total_time4 = end_time4 - start_time4

# return threshold, so_mau, subarray, array_append, values_x, mang_so_sanh, daura4, maxfinal, bin1, so_hang_lay_duoc
    return values_x, mang_so_sanh, daura4, maxfinal, bin1, total_time4
 

 

# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\Test7_2_RoI.jpg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\Led_tach_RoI.jpeg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID-cheo2.jpeg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LedID_4LED_10_07.jpg")
# img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LEDID_4_RoI_batky.jpg")
img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\LEDID_4_RoI_adjusted.jpg")



        
led1, led2, led3, led4 = process_frame(img)
print(f"led1: {led1} and led2: {led2} and led3: {led3} and led4: {led4}")