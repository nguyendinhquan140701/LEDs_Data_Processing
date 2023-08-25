import numpy as np
import time
import cv2
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def threshold(img):
    img1 = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    frame = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    print(f'frame:{frame}')
       
    select = frame[frame > 10]
    print(f"{select[:]}")
    avgValue = np.mean(select)
    print(f"avg pixel value: {avgValue}")

    height, width = frame.shape
    print(f'height:{height} and width:{width}')
    row_sorted = []
    row = []
    row2 = []
    row_sorted2 = []



    for i in range (0,height,20):
        row = sorted(frame[i], reverse=True)
        maxInRow = row[0] 
        row_sorted.append(maxInRow)
    
    for i in range (0,height):
        row2 = sorted(frame[i], reverse=True)
        maxInRow2 = row2[0] 
        row_sorted2.append(maxInRow2)

    print(f'row_sorted:{row_sorted}')

    numRow = np.zeros(len(row_sorted), dtype=int)
    for i in range (0, len(row_sorted)):
        numRow[i] = i

    numRow2 = np.zeros(len(row_sorted2), dtype=int)
    for i in range (0, len(row_sorted2)):
        numRow2[i] = i
    
    def mapping1(values_x, a0, a1, a2, a3):
        return  a3 * values_x**3 + a2 * values_x**2 + a1 * values_x + a0
    
    args, _ = curve_fit(mapping1, numRow, row_sorted)

    a_opt, b_opt, c_opt, d_opt = args

    def mapping2(values_x, a4, a5, a6, a7):
        return  a7 * values_x**3 + a6 * values_x**2 + a5 * values_x + a4
    
    args2, _ = curve_fit(mapping2, numRow2, row_sorted2)
    a_opt2, b_opt2, c_opt2, d_opt2 = args2

    print(f'a_opt, b_opt, c_opt:{a_opt}, {b_opt}, {c_opt}, {d_opt}')
    y_model = mapping1(numRow, a_opt, b_opt, c_opt, d_opt)
    y_model2 = mapping2(numRow2, a_opt2, b_opt2, c_opt2, d_opt2)

    plt.scatter(numRow, row_sorted)
    plt.plot(numRow, y_model, color = 'r')
    plt.plot(numRow2, y_model2, color = 'r')

    # plt.plot(numRow, row_sorted, color = 'blue')
    plt.plot(numRow2, row_sorted2, color = 'blue')

    plt.show()


    imgShow = cv2.resize(img1, (780,550))
    cv2.imshow("image", imgShow)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img = cv2.imread("C:\\Python\\sample\\venv\\app_proccessing_image\\ban_on_dinh\\1. doc pixel\\40cm_test2.jpeg")
threshold(img)
