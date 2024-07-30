import numpy as np
import cv2
import math
import time
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
# khai báo tham số
thresholdCount = 100 # ngưỡng xám để lọc pixel có giá trị cao
length_data = 6 # độ dãi dữ liệu đã điều chế
number_one = 4 # số bit 1 trong dữ liệu đã điều chế
length_header = 5 # độ giải mã mở đầu
nDefault = 18

class Data:
    def __init__(self, elapsed_time, w, h, x, y, code1, code2, code3, code4, check):
        self.elapsed_time = elapsed_time
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.code1 = code1
        self.code2 = code2
        self.code3 = code3
        self.code4 = code4
        self.check = check

def main(frame,height, width,threshold,nLED,id_camera):
    try:
        start_time = time.time()
        # đọc ảnh từ tập tin
        img = frame
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = cv2.convertScaleAbs(image, alpha=255.0/np.max(image))
        # goị hàm trích xuất RoI
        data_list, rois = grid_division(image, nLED,threshold,width,id_camera)
        # print(f'data_list:{data_list}')
        x=[]
        y=[]
        w=[]
        h=[]
        check = 0
        list_code = ["" for _ in range(4)]
        # giải mã dữ liệu và in kết quả
        if len(rois) == nLED:
            check = 1
            for i, data in enumerate (data_list):
                x.append(rois[i][0])
                y.append(rois[i][1])
                w.append(rois[i][2])
                h.append(rois[i][3]) 
                if data:
                    list_code[i] = decoder(data)
        end_time = time.time()
        # Tính thời gian xử lý
        elapsed_time = end_time - start_time

        cv2.imshow('Image Window', image)
        cv2.waitKey(0)

        # Close all OpenCV windows
        cv2.destroyAllWindows()
        return Data(elapsed_time, w, h, x, y, list_code[0], list_code[1], list_code[2], list_code[3],check )
    except:
        return Data(0.0,[], [], [] ,[],  str(""),str(""),str(""), str(""), 0)



# định nghĩa hàm đọc dữ liệu
def readData(bounding_boxes):
    try:
        #print(bounding_boxes)
        dark_size = [bounding_boxes[i+1][0] - bounding_boxes[i][0] - bounding_boxes[i][2] for i in range(len(bounding_boxes)-1)]
        long_size = max(dark_size)
        index =[]
        sum_header_size = 0
        for i,value in enumerate(dark_size):
            if value >= 3/4 *long_size:
                index.append(bounding_boxes[i][0]+bounding_boxes[i][2])
        for i in range(len(index)-1):
            sum_header_size += index[i+1]-index[i]
        if len(index) >=3:
            bit_size = round(sum_header_size/ (len(index)-1) / 11)
        else:
            bit_size = round(sum_header_size / 11)
        bit = []
        bit_list = []
        for i in range(1,len(bounding_boxes)):
            if 3 / 4 * long_size < dark_size[i-1] <= long_size:
                # print(bit)
                if len(bit) == length_data+2:
                    bit_list.append(bit)
                bit = []
            else:
                if bit:
                    for _ in range(math.ceil((dark_size[i-1] / bit_size))):
                        bit.append(0)
        
            for _ in range(bounding_boxes[i][2]//bit_size):
                bit.append(1)
        if len(bit_list) > 0:
            bit = bit_list[len(bit_list)//2]
        else:
            bit = []
        return bit
    except: 
        return []

# định nghĩa hàm giải mã dữ liệu
def decoder(data_decoder):
    # tiền xử lí 
    print("data_decoder:",data_decoder)
    data = []
    for bit in reversed(data_decoder[1:-1]):
        data.append(bit)
    # tiến hành giải mã
    print("data:",data)
    sk = 0
    r = number_one
    for i in range(len(data) - 1, -1, -1):
        if data[i] == 1:
            if i+1 > r:
                sk = sk + math.comb(i, r)
            r -=1
    data_4bit = format(sk, '04b')
    return data_4bit
                               
# định nghĩa hàm trích xuất RoI
def grid_division(image, nLED,threshold_read,width,id_camera):
    _, threshold_image = cv2.threshold(image, threshold_read, 255, cv2.THRESH_BINARY  )
    contours, _ = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Tính kích thước trung bình của các hình chữ nhật
    average_size = np.mean([cv2.contourArea(contour) for contour in contours])
    bounding_boxes = []
        
    # Vẽ hình chữ nhật bao quanh mỗi vân sáng trên ảnh 
    for contour in contours:
        # Tính kích thước của hình chữ nhật
        area = cv2.contourArea(contour)
        if area > average_size / 10:
            # Chỉ vẽ hình chữ nhật nếu kích thước lớn hơn 1/10 kích thước trung bình
            x, y, w, h = cv2.boundingRect(contour)
            # Lưu trữ bộ số trong danh sách
            bounding_boxes.append((x, y, w, h))

    center_array =[]
    led_area = 0
    for box in bounding_boxes:
        x,y,w,h = box
        if h > led_area:
            led_area = h
        center = (x + w // 2, y + h // 2)
        center_array.append(center)

    # Áp dụng thuật toán DBSCAN
    # dbscan = DBSCAN(eps=round(500*0.1/2), min_samples=2)
    # labels = dbscan.fit_predict(center_array)
    kmeans = KMeans(n_clusters=nLED, random_state=0)
    labels = kmeans.fit_predict(center_array)
    n = max(labels)
    data=[]
    rois=[]
    local=[]
    m = width//led_area
    if n == (nLED-1):
        list_of_contours = [[] for _ in range(nLED)]
        data=[[] for _ in range(nLED)]
        for index, value in enumerate(labels):
            if value >=0:
                list_of_contours[value].append(bounding_boxes[index])
        array_local =[2*width, width]
        for  index,contour in enumerate(list_of_contours):
            contour.sort(key=lambda box: box[0])
            data[index] = readData(contour)
            rois.append([contour[0][0],min(contour, key=lambda arr: arr[1])[1], contour[-1][0]-contour[0][0]+ contour[-1][2],max(contour, key=lambda arr: arr[3])[3]])

            if rois[index][0] < array_local[0]:
                array_local[0] = rois[index][0]
            if rois[index][1] < array_local[1]:
                array_local[1] = rois[index][1]
        for roi in rois:
            local.append((roi[1]-array_local[1])//(1.5*led_area) * m + (roi[0]-array_local[0])//(1.5*led_area) )
        if (id_camera == 1):
            for i in range(n+1):
                local[i] = (local[i]//m+1)*m - local[i]%m - 1
        # Sắp xếp theo chỉ số đầu tiên của mỗi mảng trong list_of_arrays1
        sorted_lists = sorted(zip(local,rois, data), key=lambda x: x[0])

        # Tách lại danh sách mảng 1 và mảng 2
        _,rois, data = zip(*sorted_lists)
    return data,rois

image = cv2.imread('E:\Project\OOC\LEDs_Data_Processing\LED_Decode\led_image\paper.png')
height, width, _ = image.shape
print(f'height:{height}, width:{width}')
main(image,height, width,100,4,1)    
# print(f'data:{data}')


    
            
    
