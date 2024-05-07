import numpy as np
import cv2
import matplotlib.pyplot as plt

def xu_ly_anh(img, array, Npixel):
    x1 = array[0] #ok fix 480
    y1 = array[1]
    x2 = array[2]
    y2 = array[3]

    i=0
    Pixels_Line = [] # sua duoc loi pixel line la bien public
    
##    if x2 - x1 <0:
##        Pixels_Line = np.zeros((x1-x2+1),dtype = int)
##        for x in range(x1, x2-1,-1):
##            Pixels_Line[i] = img[y1,x]
##            i = i + 1
##
##    if x2 - x1 >0:
##        Pixels_Line = np.zeros((x2-x1+1),dtype = int)
##        for x in range(x1, x2+1,+1):
##            Pixels_Line[i] = img[y1,x]
##            i = i + 1



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
    # x_list = [int(i) for i in range(N)]
    # Mang_input_waveform = np.zeros(N,dtype = float)

    # for i in range(0,N):
    #     Mang_input_waveform[i] = i/Npixel

    array_final = np.zeros(abs(y2-y1)+30, dtype = int)
    i = j = k = 0
    for k in range(0, N):
        array_final[k] = -1
    for i in range(0, N):
        if i%Npixel == 0:
            array_final[j] = Pixels_Line[i]
            j = j + 1
    # npixel_final = int(N/Npixel + 1)
    # return N, Pixels_Line, array_final, N, Mang_input_waveform, x_list
    return N, Pixels_Line, array_final, N

#-------------------------------------------------------------------
# xóa comment - phần thừa_ ok
# đầu vào ra: vào: ảnh vào, array, Npixel ok ra: kich thuoc cua line, line profile, array out, size(s), input wave form, x_list: ok sắp xếp lại ok + xóa 'print' thừa ok 
# comment import, viết def ok +return ok
# xóa thừa trước def trừ import ok, xóa print out thừa ok
