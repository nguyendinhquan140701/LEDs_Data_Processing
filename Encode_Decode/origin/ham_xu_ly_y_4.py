
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def xu_ly_y(array2, values_y, row, threshold_code, input_var):
    values_x = [int(i) for i in range(len(values_y))] 
    mse_y_values = [int(i) for i in range(len(values_y))] 

    def mapping1(values_x, a0, a1, a2, a3):
        return a3 * values_x**3 + a2 * values_x**2 + a1 * values_x + a0

    args, _ = curve_fit(mapping1, values_x, values_y)

    mse_final = 0
    for i in range(0,len(values_y)):
        mse_y = args[0] + args[1]*i + args[2]*i**2 + args[3] * i**3
        mse = ((values_y[i] - mse_y)**2)/len(values_y)
        mse_final += mse 
        mse_y_values[i] = mse_y 

    mang_so_sanh = [int(i) for i in range(len(values_y))] 
    so_sanh = 0
    for i in range(0,len(values_y)):
        if values_y[i] >= mse_y_values[i]:
            so_sanh = 1
        else:
            so_sanh = 0
        mang_so_sanh[i] = so_sanh

    if len(mang_so_sanh) >= len(array2[0]):
        c = np.pad(array2, [(0, 0),(0, len(mang_so_sanh) - len(array2[0]))], mode='constant')
        array_append = np.append([mang_so_sanh],c,axis=0)
    else:
        c = np.pad(mang_so_sanh, (0, len(array2[0]) - len(mang_so_sanh)), 'constant')
        array_append = np.append([c],array2,axis=0)

    so_hang_lay_duoc = len(array_append[0])
    if so_hang_lay_duoc <= row:
        subarray = array_append
    else:
        subarray = array_append[0:row]

    a_man = []

    for i in range(0, len(threshold_code)):
        if threshold_code[i] == 1:
            a_man = np.append(a_man, [0,1])
        else:
            a_man = np.append(a_man, [1,0])
    a_man = list(map(int, a_man))
    so_mau = len(subarray)*len(subarray[0])

    n = len(values_y)
    s = 0
    for i in range(n):
        s = s + values_y[i]
    threshold = s/n

    mang_2d_dau_vao = subarray
    if np.size(mang_2d_dau_vao,0) < row:
        n_loop = np.size(mang_2d_dau_vao,0)
    else:
        n_loop = row
    c = np.size(mang_2d_dau_vao,1)  
    d = np.size(threshold_code)
    b = threshold_code
    MANG = np.zeros((n_loop,20), dtype = int) 
    MANG_index = np.zeros((n_loop,20), dtype = int)
    MANG_test = np.zeros((n_loop,20), dtype = int)
    MANG_heso = np.zeros((n_loop,20), dtype = int)
    MANG_daura = np.zeros(n_loop, dtype = int)

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

    for i_loop in range(0, n_loop):
        a = mang_2d_dau_vao[i_loop]
        i = 0
        n = 0
        for k in range(0,20):
            x[k] = -1
        for j in range(0, c-d+1):
            for m in range(0, d-input_var):
                n = n + abs(a[j+m] - b[m])
            if n == 0:
                for o in range(0, input_var):
                    # print("i,j,d,o, trong1, trong2", i,j,d,o, i+o, j+d-input_var+o)
                    if i + 0 < 20:  #ok fix xong 20. ctr chạy êm ru.
                        x[i + o] = a[j+d-input_var+o]
                    else:
                        pass

                i = i + input_var
            n = 0

        MANG[i_loop] = x
        for k2 in range(0, sizeb):
            heso[k2] = -1
            kiemtra[k2] = -1
        for i2 in range(0, sizeb - input_var, 2):
            if x[i2] == -1: 
                break
            else:
                heso[int(i2/2)] = 0
                for j2 in range (0, input_var):
                    heso[int(i2/2)] = heso[int(i2/2)] + x[i2+j2]*(1 << j2)
                    kiemtra[i2] = 1 << j2
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
       
        MANG_index[i_loop] = index
        MANG_test[i_loop]  = test
        MANG_heso[i_loop]  = heso

        max1_3 = 0
        value3 = -1
        for i3 in range(0, size):
            if index[i3] > max1_3:
                max1_3 = index[i3]
                value3 = test[i3]
        daura = value3
        MANG_daura[i_loop] = daura 

    array = [input_var]*n_loop
    size4 = np.size(MANG_daura)

    test4 = np.zeros(20, dtype = int)
    index4 = np.zeros(20, dtype = int)

    count4 = countdem4 = max1_4 = max2_4 = daura4 = value4 = 0
    max3_4 = maxfinal = index3_4 = indexfinal = 0

    for l4 in range(0,20):
        test4[14] = -1
        index4[14] = -1

    max1_4 = 0
    countdem4 = 0
    size4 = len(MANG_daura)
    for m4 in range(0, size4):
        count4 = 0
        countdem4 = 0
        for n4 in range(0, 20):
            if MANG_daura[m4] == test4[n4] or MANG_daura[m4] == -1:
                count4 = 1
        if count4 != 1:
            for o4 in range(0,size4):
                if MANG_daura[m4] == MANG_daura[o4]:
                    countdem4 = countdem4 + 1
            index4[max1_4] = countdem4
            test4[max1_4] = MANG_daura[m4]
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
    bin1 = twosCom_decBin(value4, 32) 
    bin1 = str(bin1)[::-1] 
    bin1 = [int(i) for i in str(bin1)] 
    bin1 = bin1[0:digit]
    return threshold, so_mau, subarray, array_append, values_x, mang_so_sanh, daura4, maxfinal, bin1, so_hang_lay_duoc

#------------------------------------------------------------------------
# xóa comment - phần thừa_ ok
# đầu vào ra giống labview:
#       vào: Array 2 = array2, Array in = values_y, row, threshold code = threshold_code, data number = input_var ok ? vào trong chương trình chính không có threshold code 3 nhưng c.trình con lại có - thực sự khi chạy với cam, 
# threshold code 3 không hiện giá trị coi như tập rỗng và trong python chỉ mục đích nối vào mảng sau manchester, do đó, xóa toàn bộ l.quan threshold code 3 trong python
#       ra: threshold, số mẫu, datamatrix = subarray, Array = array_append, Sine with uniform Noise(do thi values_x, mang_so_sanh), probablility, Appearance times, Data value = bin1, so hang lay duoc: ok
#       sắp xếp lại ok + xóa 'print' thừa ok
# comment import, viết def ok +return ok
# xóa thừa trước def trừ import ok, xóa print out thừa ok
