
import numpy as np
import cv2
def ve_roi(img, text, array, x):
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
    return img

#----------------------------------------------------------
# xóa comment - phần thừa_ ok
# đầu vào ra: vào: ảnh, text, array, x ok ra: ảnh ra: ok sắp xếp lại ok + xóa 'print' thừa ok 
# comment import, viết def ok +return ok
# xóa thừa trước def trừ import ok, sau return ok , xóa print out thừa ok
