import cv2
import numpy as np
import ham_ve_roi_4 as hvr
import ham_check_roi_tu_arr_6_5 as hc

image = cv2.imread("C:\\Python\\sample\\venv\\ban_on_dinh\\1. doc pixel\\anh 1800_1001.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

width = image.shape[1]
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
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)
    top.append(int(y))
    bot.append(int(y+h))
#    print("lennnnnnn",len(contours))


#-------------------------------------------------------------------------------------------------------------------------------
# a, b = hc.check_roi_tu_arr(mass_centres_x, mass_centres_y, top, bot)

str_x = mass_centres_x
Y = mass_centres_y
top = top
bot = bot


print("str_x\n", str_x)
print(len(str_x))
print("Y    \n", Y)
print("top\n", top)
print(len(top))
print("bot\n", bot)





j = 1
k = 0
str_out1 = np.zeros((50, 4), dtype = int)
str_out2 = np.zeros((50, 4), dtype = int) 
str_out3 = np.zeros((50, 4), dtype = int)
str_out4 = np.zeros((50, 4), dtype = int) 

str_out5 = np.zeros((50, 4), dtype = int)
str_out6 = np.zeros((50, 4), dtype = int)
str_out7 = np.zeros((50, 4), dtype = int)
str_out8 = np.zeros((50, 4), dtype = int)

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
                


n = 50
i1 = i2 = i3 = i4 = 0
j1 = j2 = j3 = j4 = 0
tg = 0
a = b = c = 0
max1 = max2 = max3 = max4 = 0
x_top = x_bot = 0
x_top2 = x_bot2 = 0
min1 = min2 = min3 = min4 = 0


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

for a in range(0, 3):
    for b in range(a+1, 4):
        if str_[a] < str_[b]:
            tg = str_[a]
            str_[a] = str_[b]
            str_[b] = tg

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
    str_outout1[0] = (x_top + x_bot)/2
    str_outout1[1] = min1
    str_outout1[2] = (x_top + x_bot)/2
    str_outout1[3] = max1
    
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

    print("xtop", x_top)
    print("xbot", x_bot)
    print("min1", min1)
    print("max1", max1)




    
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



#-------------------------------------------------------------------------------------------------------------------------------
if a[0] == a[1] == a[2] == a[3] ==0 or abs(a[1]-a[3]>=480): #ok fix 480
    a = [0,0,0,103]
if b[0] == b[1] == b[2] == b[3] ==0 or abs(a[1]-a[3]>=480):
    b = [0,0,0,103]
#        print("roi1,roi2", a,b)

text1 = 'RoI'
#        text2 = 'r2'
x = width
print("a1", a)
l1 = a[0]
l2 = a[1]
l3 = a[2]
l4 = a[3]
# a[0] = l2
# a[1] = l1
# a[2] = l4 #l4
# a[3] = l3 

a[0] = l1
a[1] = l2
a[2] = l3 #l4
a[3] = l4 
print("a2", a)
image = hvr.ve_roi(image, text1, a, x) 







color = image[330, 220]
# cv2.imwrite('anh_RoI_len_contours'+'.jpg',image)
cv2.imshow("image", image)

cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image


# if image type is b g r, then b g r value will be displayed.
# if image is gray then color intensity will be displayed.
print(color)

# bin = 0
