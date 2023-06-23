# import the opencv library
import cv2
# import ham_check_roi_tu_arr_6_5 as hc
import ham_ve_roi_4 as hvr
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import ham_xu_ly_anh_xam as hxla
# import ham_xu_ly_y_4 as xly
import time
from sklearn.metrics import mean_squared_error


start_time_total = time.time()

# vid = cv2.VideoCapture(0)
# vid.set(cv2.CAP_PROP_EXPOSURE, -13)
# # vid.set(3, 640)
# # vid.set(4, 480)
# array2 = [[0]]
bien_nho_max = 0
bien_nho_so_anh = 0
mang_so_1 =[0]
mang_so_1_append = []

# while(True):

array2 = [[0]] # TH khong can tinh xac suat
img = cv2.imread("C:\\Python\sample\\venv\\ban_on_dinh\\1. doc pixel\\test7.jpeg")
# print(img)

img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #
#    cv2.imshow("Frame", img) # raw


height = frame.shape[0]
width = frame.shape[1]
# print("height, width", height, width)

ret, frame0 = cv2.threshold(frame, 200, 255, cv2.THRESH_BINARY)
# cv2.imshow("Frame", frame0)
contours, hierarchy = cv2.findContours(frame0, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)

# contours = sorted(contours, key=cv2.contourArea, reverse=True)

# print(len(contours[0]), " so sanh", len(contours[1]))
# if len(contours) > 50:
#     contours = contours[0:50]


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
if len(contours) == 0 or len(contours) > 2000:
       contours = contours[0:45]

# print(contours)


mass_centres_x = []
mass_centres_y = []
top = []
bot = []

print("lennnnnnn",len(contours))

# xác định được tâm của từng contour
for i in range(0, len(contours)):
    M = cv2.moments(contours[i], 0)
    if M["m00"] != 0:
        mass_centres_x.append(int(M['m10']/M['m00']))
        mass_centres_y.append(int(M['m01']/M['m00']))
    else:
        mass_centres_x.append(int(0))
        mass_centres_y.append(int(0))



# vẽ hình chữ nhật của contour và xác định được cạnh top, bot
for i in range(0, len(contours)):
    x,y,w,h = cv2.boundingRect(contours[i])
    # cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
    top.append(int(y))
    bot.append(int(y+h))

    # top.append(int(x))
    # bot.append(int(x+w))
    
# if len(contours) == 0 or len(contours) >= 50:
#    pass

# tranh loi 
else:
    if len(mass_centres_x) == 0:
        mass_centres_x = np.zeros(1, dtype=int)
    if len(mass_centres_y) == 0:
        mass_centres_y = np.zeros(1, dtype=int)
    if len(top) == 0:
        top = np.zeros(1, dtype=int)
    if len(bot) == 0:
        bot = np.zeros(1, dtype=int)
    #------------------------------------------------------------------------------------------------------------------
# gop check_roi_tu_arr
#        a, b = hc.check_roi_tu_arr(mass_centres_x, mass_centres_y, top, bot)

## xu ly toi da 50 contour; x,y, top , bot
    str_x = mass_centres_x
    Y = mass_centres_y
    top = top
    bot = bot

  
    k = 0

    # chia làm 8 phần của 1 frame để lọc tâm từng phần, mỗi phần sẽ có 1 mảng để chứa 4 đầu vào x,y, top, bot
    str_out1 = np.zeros((50, 4), dtype = int)
    str_out2 = np.zeros((50, 4), dtype = int) 
    str_out3 = np.zeros((50, 4), dtype = int)
    str_out4 = np.zeros((50, 4), dtype = int) 

    str_out5 = np.zeros((50, 4), dtype = int)
    str_out6 = np.zeros((50, 4), dtype = int)
    str_out7 = np.zeros((50, 4), dtype = int)
    str_out8 = np.zeros((50, 4), dtype = int)

    n = len(str_x)
    j = 1
    max1 = str_x[0]
    min1 = str_x[0]


    
    # khai bao 4 đầu vào của 1 mảng 2 chiều str_out1 : x, y, top, bot để lọc tâm
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
    # sau khi lọc xong lần 1, các tâm không thỏa mãn sẽ được lọc tiếp lần 2
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

    # khai bao de xu ly 1,3,5,7 với 4 giá trị : (x1,y1) và (xn, yn)
    str_outout1 = np.zeros(4, dtype = int) # den 1: 
    str_outout2 = np.zeros(4, dtype = int) # den 2
                    
  


    # Xu ly tam str_out 1.3.5.7
    n = 50
    i1 = i2 = i3 = i4 = 0
    j1=j2=j3=j4=0
    tg = 0
    a = b = c = 0
    max1 = max2 = max3 = max4 = 0
    x_top = x_bot = 0
    x_top2 = x_bot2 = 0 # den 2
    min1 = min2 = min3 = min4 = 0 

    start_time = time.time()

    # dem so phần tử mà toa do của tâm contour (x,y) của str_out 1,3,5,7 khác 0
    # in1[i1][0] : x_tam
    # in1[i1][1] : y_tam
    for i1 in range(0, 50):
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

    # sắp xếp số phần tử vừa dếm để sử dụng 2 mảng có số lượng contour lớn nhất 
    for a in range(0, 3):
        for b in range(a+1, 4):
            if str_[a] < str_[b]:
                tg = str_[a]
                str_[a] = str_[b]
                str_[b] = tg

    # truong hop co 1 den
    if str_[0] == j1:
        max1 = 0
        min1 = in1[0][3] # = bot

        # so sanh chay het cac gia tri của contour thỏa mãn ->  chay điểm đầu đến điểm cu
        for i2 in range(0, j1):
            if in1[i2][2] > max1:    # xet giá trị của x_top
                max1 = in1[i2][2]
                x_top = in1[i2][0]
            if in1[i2][3] <= min1:
                min1 = in1[i2][3]
                x_bot = in1[i2][0]
        str_outout1[0] = (x_top + x_bot)/2  # (x0 + x3) / 2
        str_outout1[1] = min1 # = t0: theo truc oy
        str_outout1[2] = (x_top + x_bot)/2  # 
        str_outout1[3] = max1 # = b3 : \theo truc oy
        
    if str_[0] == j2:
        max1 = 0
        min1 = in2[0][3]
        for i2 in range(0, j2):
            if in2[i2][2] > max1:
                max1 = in2[i2][2]
                x_top = in2[i2][0]
            if in2[i2][3] <= min1:
                min1 = in2[i2][3]
                x_bot = in2[i2][0]
        str_outout1[0] = (x_top + x_bot)/2
        str_outout1[1] = min1
        str_outout1[2] = (x_top + x_bot)/2
        str_outout1[3] = max1
        
    if str_[0] == j3:
        max1 = 0
        min1 = in3[0][3]
        for i2 in range(0, j3):
            if in3[i2][2] > max1:
                max1 = in3[i2][2]
                x_top = in3[i2][0]
            if in3[i2][3] <= min1:
                min1 = in3[i2][3]
                x_bot = in3[i2][0]
        str_outout1[0] = (x_top + x_bot)/2
        str_outout1[1] = min1
        str_outout1[2] = (x_top + x_bot)/2
        str_outout1[3] = max1

    if str_[0] == j4:
        max1 = 0
        min1 = in4[0][3]
        for i2 in range(0, j4):
            if in4[i2][2] > max1:
                max1 = in4[i2][2]
                x_top = in4[i2][0]
            if in4[i2][3] <= min1:
                min1 = in4[i2][3]
                x_bot = in4[i2][0]
        str_outout1[0] = (x_top + x_bot)/2
        str_outout1[1] = min1
        str_outout1[2] = (x_top + x_bot)/2
        str_outout1[3] = max1

    # truong hop co den so 2
    if str_[1] == j1:
        max2 = 0
        min2 = in1[0][3]
        for i3 in range(0, j1):
            if in1[i3][2] > max2:
                max2 = in1[i3][2]
                x_top2 = in1[i3][0]
            if in1[i3][3] <= min2:
                min2 = in1[i3][3]
                x_bot2 = in1[i3][0]
        str_outout2[0] = (x_top2 + x_bot2)/2
        str_outout2[1] = min2
        str_outout2[2] = (x_top2 + x_bot2)/2
        str_outout2[3] = max2

    if str_[1] == j2:
        max2 = 0
        min2 = in2[0][3]
        for i3 in range(0, j2):
            if in2[i3][2] > max2:
                max2 = in2[i3][2]
                x_top2 = in2[i3][0]
            if in2[i3][3] <= min2:
                min2 = in2[i3][3]
                x_bot2 = in2[i3][0]
        str_outout2[0] = (x_top2 + x_bot2)/2
        str_outout2[1] = min2
        str_outout2[2] = (x_top2 + x_bot2)/2
        str_outout2[3] = max2

    if str_[1] == j3:
        max2 = 0
        min2 = in3[0][3]
        for i3 in range(0, j3):
            if in3[i3][2] > max2:
                max2 = in3[i3][2]
                x_top2 = in3[i3][0]
            if in3[i3][3] <= min2:
                min2 = in3[i3][3]
                x_bot2 = in3[i3][0]
        str_outout2[0] = (x_top2 + x_bot2)/2
        str_outout2[1] = min2
        str_outout2[2] = (x_top2 + x_bot2)/2
        str_outout2[3] = max2

    if str_[1] == j4:
        max2 = 0
        min2 = in4[0][3]
        for i3 in range(0, j2):
            if in4[i3][2] > max2:
                max2 = in4[i3][2]
                x_top2 = in4[i3][0]
            if in4[i3][3] <= min2:
                min2 = in4[i3][3]
                x_bot2 = in4[i3][0]
        str_outout2[0] = (x_top2 + x_bot2)/2
        str_outout2[1] = min2
        str_outout2[2] = (x_top2 + x_bot2)/2
        str_outout2[3] = max2

    a = str_outout1
    b = str_outout2

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("elapsed time:", elapsed_time)

    if a[0] == a[1] == a[2] == a[3] ==0 or abs(a[1]-a[3]>=480) or a[1] == 480 or a[3] == 480: #ok fix 480
        a = [0,0,0,103]
    if b[0] == b[1] == b[2] == b[3] ==0 or abs(a[1]-a[3]>=480):
        b = [0,0,0,103]
#-----------------------------------------------------------------------------------------------------------------------
    print("roi1", a)
    print("roi2", b)

    text1 = 'RoI'
    text2 = 'r2'
    x = width

#----------------------------------------------------------------------------------------------------------------------
# gop module ve_roi
    img = img
    text = text1
    array = a
    array_roi2 = b

    x = x

    x1 = array[0]
    x2 = array[1]
    x3 = array[2]
    x4 = array[3]

    x5 = array_roi2[0]
    x6 = array_roi2[1]
    x7 = array_roi2[2]
    x8 = array_roi2[3]

    y1 = 0 #
    y2 = x4

    if x3 + 10 > x:
        y1 = x3 - 15
    else:
        y1 = 5 + x3


    
    # y3 = 0
    # y4 = x8

    # if x7 + 10 > x:
    #     y1 = x3 - 15
    # else:
    #     y1 = 5 + x3    

    img = cv2.line(img,(x1,x2),(x3,x4),(0,0,255),1,cv2.LINE_AA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.putText(img, text, (y1,y2), font, 1.5, (0,0,255),2,cv2.LINE_AA)



    frame2 = img

 
    # frame2 = hvr.ve_roi(img, text1, a, x) 
    # frame2 = hvr.ve_roi(img, text2, b, x)



#-----------------------------------------------------------------------------
    Npixel = 11

    array = a

#-----------------------------------------------------------------------------
# gop module xu_ly_anh
    img = frame
    array = array
    Npixel = Npixel


    x1 = array[0] #ok fix 480
    y1 = array[1]
    x2 = array[2]
    y2 = array[3]
    print(y1, "and", y2)

    i=0
    Pixels_Line = [] # sua duoc loi pixel line la bien public
    
    # if x2 - x1 <0:
    #     Pixels_Line = np.zeros((x1-x2+1),dtype = int)
    #     for x in range(x1, x2-1,-1):
    #         Pixels_Line[i] = img[y1,x]
    #         i = i + 1

    # if x2 - x1 >0:
    #     Pixels_Line = np.zeros((x2-x1+1),dtype = int)
    #     for x in range(x1, x2+1,+1):
    #         Pixels_Line[i] = img[y1,x]
    #         i = i + 1



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


            

    N = len(Pixels_Line) 
    print("N:", N)
    # x_list = [int(i) for i in range(N)]
    # Mang_input_waveform = np.zeros(N,dtype = float)

    # for i in range(0,N):
    #     Mang_input_waveform[i] = i/Npixel

    array_final = np.zeros(abs(y2-y1)+10, dtype = int)
    i = j = k = 0
    for k in range(0, N):
        array_final[k] = -1
    for i in range(0, N):
        if i%Npixel == 0:
            array_final[j] = Pixels_Line[i]
            j = j + 1

            
    npixel_final = int(N/Npixel + 1)

    c0 = array_final
    print("gia tri pixel:", c0[100])
    print("len mang xam: ", len(c0))
    print("len cac bit: ", npixel_final)

    
#        a0,b0,c0,d0,e0,f0 = hxla.xu_ly_anh(frame, array, Npixel)
#-----------------------------------------------------------------------------
    # print("Kich thuoc cua line", a0)
#        plt.plot(f0, b0) 
#        plt.show()
#        print('output_variable = Array out = decimated array: ', c0)
#        print("size(s): ", d0)
#        plt.plot(e0, b0)
#        plt.show()

  
    values_y = c0 # mảng giá trị của ảnh xám RoI đi qua
    row = 100 # để tính xác suất với 100 ảnh gần nhất
    threshold_code = [0,1,1,1,0,0,1,0,0,1]
    input_var = 4
#--------------------------------------------------------------------------------------------------------
# gop module xu_ly_y        
#        a00, a1, a2, a3, a4, a5, a6, a7, a8, a9 = xly.xu_ly_y(array2, values_y, row, threshold_code, input_var)

    array2 = array2
    values_y = values_y
    row = row
    threshold_code = threshold_code
    input_var = input_var
    
    print("len values_y: ", len(values_y))
    values_x = [int(i) for i in range(len(values_y))] 
    values_x = np.zeros(len(values_y), dtype=int)
    for k in range(0, len(values_y)):
        values_x[k] = k
    # print("value_X: ", values_x[:50])

    # print("value_Y: ", values_y[:50] )

    # ve curve fit
    def mapping1(values_x, a0, a1, a2, a3):
        return a3 * values_x**3 + a2 * values_x**2 + a1 * values_x + a0
    args, _ = curve_fit(mapping1, values_x, values_y)

    # print(f"a3: {args[1]}")

    a_opt, b_opt, c_opt, d_opt = args
    y_model = mapping1(values_x, a_opt, b_opt, c_opt, d_opt)
    mse = mean_squared_error(values_y, y_model)
    print(mse)
    plt.scatter(values_x, values_y)
    plt.plot(values_x, y_model, color = 'r')
    plt.plot(values_x, values_y, color = 'blue')
    plt.show()         

    # len(values_y) là phụ thuộc người đặt khi khai báo array_final = np.zeros(500, dtype = int) ở trên
    # so sánh giá trị dự đoán: mse_y khi có optimal value(a0, a1, a2, a3) với giá trị thực tế: values_y
    mse_y_values = [int(i) for i in range(len(values_y))] 
    mse_final = 0
    for i in range(0,len(values_y)):
        mse_y = args[0] + args[1]*i + args[2]*i**2 + args[3] * i**3
        # mse_y = args[0] + args[1]*i
        mse = ((values_y[i] - mse_y)**2)/len(values_y)
        mse_final += mse 
        mse_y_values[i] = mse_y 

    print(f"mse_final: {mse_final}")


    # print("gia tri du doan: ", mse_y_values[:], "va gia tri thuc te: ", values_y[:])
 
    # chuyen sang 0; 1
    mang_so_sanh = [int(i) for i in range(len(values_y))] 
    so_sanh = 0
    for i in range(0,len(values_y)):
        if values_y[i] >= mse_y_values[i]:
            so_sanh = 1
        else:
            so_sanh = 0
        mang_so_sanh[i] = so_sanh
    #end

    print(mang_so_sanh[:])
    #s
    # array2 = [[0]]

    # mở rộng kích thước của array2 có size là [1, len(mang_so_sanh)], nghĩa là:  row: 1 -  column: len(value_y)
    # if len(mang_so_sanh) >= len(array2[0]):
    #     c = np.pad(array2, [(0, 0),(0, len(mang_so_sanh) - len(array2[0]))], mode='constant')

    #     array_append = np.append([mang_so_sanh],c,axis=0) # nối theo chiều dọc hai mảng vào với nhau, thành mảng 2 chiều: row: 2 - column: len(value_y)
        
        # print("value array:", array_append)
        # print("size:", array_append.shape)
    # else:
    #     c = np.pad(mang_so_sanh, (0, len(array2[0]) - len(mang_so_sanh)), 'constant')
    #     array_append = np.append([c],array2,axis=0)
    #end

    # print("array_append:", array_append)
    # so_hang_lay_duoc = len(array_append[0]) # tính len của hàng đầu tiên
    # print("len(so_hang_lay_duoc)", so_hang_lay_duoc)
    # print("row:", row)

    row = 100
    # if so_hang_lay_duoc <= row:  # row = 100 . Tại sao phải kiếm tra ?
    #     subarray = array_append  # lưu array_append sang 1 array khác
    # else:
    #     subarray = array_append[0:row]
    # print("len(subarray): ", len(subarray))
    # print("len(array_append[0:row]): ", len(array_append[0:row]))


    # sử dụng manchester từ labview
    # a_man = []
    # threshold_code = [0,1,1,1,0,0,1,0,0,1]
    # for i in range(0, len(threshold_code)):
    #     if threshold_code[i] == 1:
    #         a_man = np.append(a_man, [0,1])
    #     else:
    #         a_man = np.append(a_man, [1,0])

    # a_man = list(map(int, a_man))
    
    # so_mau = len(subarray)*len(subarray[0])
    # print("so mau:", so_mau)
    #end


    # n = len(values_y) # values_y = mảng giá trị của ảnh xám RoI đi qua
    # s = 0
    # for i in range(n):
    #     s = s + values_y[i]
    # print("s: ", s)  
    # threshold = s/n
    # print("threshold", threshold)

    mang_2d_dau_vao = mang_so_sanh
    # print("mang_2d_dau_vao", np.size)
    # if np.size(mang_2d_dau_vao,0) < row:
    #     n_loop = np.size(mang_2d_dau_vao,0) # hàm trả về số hàng của mang_2d_dau_vao and = 2
    # else:
    #     n_loop = row # row = 100
    
    n_loop = 1
    print("n_loop: ", n_loop)
    c = np.size(mang_2d_dau_vao)  # hàm trả về số cột của mang_2d_dau_vao and = 500
    # print("c:",c)
    d = np.size(threshold_code) # return số phần tử của threshold_code = 10
    b = threshold_code  #  threshold_code = [0,1,1,1,0,0,1,0,0,1]

    print("d:", d)
    MANG = np.zeros(20, dtype = int) #  column = 20
    MANG_index = np.zeros(20, dtype = int)
    MANG_test = np.zeros(20, dtype = int)
    MANG_heso = np.zeros(20, dtype = int)
    MANG_daura = np.zeros(n_loop, dtype = int) # sô phần tử = n_loop

    i = j = k = m = n = o = 0
    x = np.zeros(20, dtype = int) # mảng cứ giống 6 bit đầu giống hoàn toàn threshold thì lấy 4 bít cuối trong mảng 100
    heso = np.zeros(20, dtype = int)
    test = np.zeros(20, dtype = int)
    index = np.zeros(20, dtype = int)
    kiemtra = np.zeros(20, dtype = int)
    count = countdem = max1 = 0
    sizeb = 20
    max1_3 = 0
    value = -1
    size = sizeb 
# 3 loop:
    # start_time = time.time()
    # print("a[2]", mang_2d_dau_vao[2])
    # for i_loop in range(0, n_loop ):

    # print("gia tri mang a:", mang_2d_dau_vao)


    a = mang_2d_dau_vao

    print("gia tri len mang a:", len(mang_2d_dau_vao))
    i = 0
    n = 0
    dem_n = 0
    for k in range(0,20):
        x[k] = -1
    for j in range(0, c-d+1):  # c = 500, d= 10
        for m in range(0, d-input_var): # d-input_var = 10-4=6
            n = n + abs(a[j+m] - b[m])  # b = threshold_code
            # if abs(a[j+m] - b[m]) == 0 and n == 0:
            #     print(f"gia tri J =  {j} , m = {m}, gia tri n = {n}") 
        if n == 0:
            # print(f"gia tri J: {j} va m: {m} va dem_n: {dem_n}")
            for o in range(0, input_var):
                # print("i,j,d,o, trong1, trong2", i,j,d,o, i+o, j+d-input_var+o)
                if i + o < 20:  #ok fix xong 20. ctr chạy êm ru.
                    x[i + o] = a[j+d-input_var+o]
                    
                else:
                    pass

            i = i + input_var
        n = 0

    print("x:", x)
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print("elapsed time:", elapsed_time)


    MANG = x
    for k2 in range(0, sizeb):
        heso[k2] = -1
        kiemtra[k2] = -1
    for i2 in range(0, sizeb - input_var, 2):
        print(f"gia tri i2: {i2}")
        if x[i2] == -1: 
            break
        else:
            heso[int(i2/2)] = 0
            print(f"heso: {heso}")
            for j2 in range (0, input_var):
                heso[int(i2/2)] = heso[int(i2/2)] + x[i2+j2]*(1 << j2)
                # print(f"heso trong for 2: {heso}")
                kiemtra[i2] = 1 << j2
                # print(f"kiem tra array: {kiemtra}") 
    
    print(f"heso sau khi dich bit: {heso}")
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


    MANG_index = index
    MANG_test  = test
    MANG_heso = heso

    max1_3 = 0
    value3 = -1
    for i3 in range(0, size):
        if index[i3] > max1_3:
            max1_3 = index[i3]
            value3 = test[i3]
    daura = value3
    print("value3:", value3)
    MANG_daura = daura 
    print("mangdaura:", MANG_daura)

    # end_time = time.time()

    # elapsed_time = end_time - start_time
    # print("elapsed time:", elapsed_time)

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
        if MANG_daura == test4[n4] or MANG_daura == -1:
            count4 = 1
    if count4 != 1:
        # for o4 in range(0,size4):
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
             print(bin1)
        while len(bin1)<digit :
                bin1 = '0'+bin1
                return bin1
        else:
            bin1 = -1*dec
        return bin(bin1-pow(2,digit)).split("0b")[1]
    bin1 = twosCom_decBin(value4, 32) 
    bin1 = str(bin1)[::-1] 
    bin1 = [int(i) for i in str(bin1)] 
    bin1 = bin1[0:digit]


    a6 = daura4
    a8 = bin1


end_time_total = time.time()
total_time = end_time_total - start_time_total
print("total_time:", total_time)


#----------------------------------------------------------------------------------------------------------------
#        print("threshold: ",a00)
#        print("số mẫu: ", a1)
#        print("data matrix: ", a2)
#        print("Array: ", a3)
#        plt.plot(a4, a5)
#        plt.show()
##        print("xac suat nhan dang dung cua den 1:", int(a6))
#        print("so lan xuat hien:", a7)
print("du lieu giai ma tu den", a8, "\n")
    
#        print("so hang lay duoc: ", a9)

    # if a8 == threshold_code[len(threshold_code)-input_var:len(threshold_code)]:
    #     mang_so_1_append = 1
    # else:
    #     mang_so_1_append = 0
    # mang_so_1 = np.append(mang_so_1_append, mang_so_1)


    
##        print('mang_so_1', mang_so_1)


    # if len(mang_so_1) <= row-1:
    #     mang_so_1 = mang_so_1

    # else:
    #     mang_so_1 = mang_so_1[0:row]

    # tong_so_1 = np.count_nonzero(mang_so_1 == 1)
    
    # a6 = (tong_so_1)*100/len(mang_so_1)
#        print('tong_so_1', tong_so_1)
#
#
#        print('len_mang_so_1', len(mang_so_1))
#        
    
#        print('array2', array2)
    # if len(a3) <= row:
    #    array2 = a3
    # else:
    #    array2 = a3[0:row]
    # bien_nho_so_anh = bien_nho_so_anh + 1
#        if aa == 600:
##        print(bien_nho_so_anh)
    # Display the resulting frame
#        cv2.imshow('frame', img)
#---------------------------------------------------------------
# xu ly bien nho:
    # if a6 > bien_nho_max:
    #     bien_nho_max = a6
#        print("bien nho", a6)
#---------------------------------------------------------------

font = cv2.FONT_HERSHEY_SIMPLEX

    # frame2= cv2.putText(frame2, "Xac suat nhan dang dung cua den (%):", (0,385),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
    # frame2= cv2.putText(frame2, str(int(a6)), (10,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)

    # frame2= cv2.putText(frame2, "(max", (45,410),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu

    # frame2= cv2.putText(frame2, str(int(bien_nho_max)), (100,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)
    # frame2= cv2.putText(frame2, ")", (140,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)        
    
# frame2= cv2.putText(frame2, "Du lieu giai ma tu den:", (0,450),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
# frame2= cv2.putText(frame2, str(a8), (10,475),font, 0.7, (0,0,255),2,cv2.LINE_AA)

    # print(a8)

    # frame2= cv2.putText(frame2, "So anh da xu ly:", (450,450),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
    # frame2= cv2.putText(frame2, str(bien_nho_so_anh), (460,475),font, 0.7, (0,0,255),2,cv2.LINE_AA)
    
    # et = time.time()

    # elapsed_time = round(et - st,2)

    # frame2= cv2.putText(frame2, "Thoi gian (s):", (450, 385),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
    # frame2= cv2.putText(frame2, str(elapsed_time), (460,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)


frame2 = cv2.resize(frame2,(780,550))
cv2.imshow("Frame", frame2)
    

    # if cv2.waitKey(1) & 0xFF == ord('p'):
cv2.waitKey(0)



    # get the execution time

#        print('time', elapsed_time)

# vid.release()
cv2.destroyAllWindows()

#--------------------------------------------------
# xóa comment thừa ok
# xóa height: ok
# sửa tối ưu vào module xla ok
# xóa đặt trùng tên ok
# xóa các lệnh thừa trùng lặp
# chỉnh xla xám về 100 để không bị lỗi, đặt lại đ.kiện N
