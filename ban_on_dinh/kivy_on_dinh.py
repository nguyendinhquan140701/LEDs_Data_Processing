from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import ham_check_roi_tu_arr_6_5 as hc
import ham_ve_roi_4 as hvr
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import ham_xu_ly_anh_xam as hxla
import ham_xu_ly_y_4 as xly


class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, img = self.capture.read()
        
        if ret:
            
            array2 = [[0]]
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #
        #    cv2.imshow("Frame", img) # raw


        #    height = frame.shape[0]
            width = frame.shape[1]
        #     print("height, width", height, width)

            ret, frame0 = cv2.threshold(frame, 230, 255, cv2.THRESH_BINARY)
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
            if len(contours) == 0 or len(contours) >= 500:
                pass
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
        #    print("lennnnnnn",len(contours))

                
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
                if a[0] == a[1] == a[2] == a[3] ==0:
                    a = [0,0,0,103]
                if b[0] == b[1] == b[2] == b[3] ==0:
                    b = [0,0,0,103]
        #        print("roi1,roi2", a,b)

                text1 = 'RoI'
        #        text2 = 'r2'
                x = width
                frame2 = hvr.ve_roi(img, text1, a, x) 
        #        frame2 = hvr.ve_roi(img, text2, b, x)



        #-----------------------------------------------------------------------------
                Npixel = 4

                array = a


                a0,b0,c0,d0,e0,f0 = hxla.xu_ly_anh(frame, array, Npixel)

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
                print("xac suat nhan dang dung cua den 1:", int(a6))
        #        print("so lan xuat hien:", a7)
                print("du lieu giai ma tu den", a8, "\n")
                
        #        print("so hang lay duoc: ", a9)

                if len(a3) <= row:
                    array2 = a3
                else:
                    array2 = a3[0:row]
        #        aa = aa + 1
        #        if aa == 600:
        #            print(aa)
                # Display the resulting frame
        #        cv2.imshow('frame', img)
        #---------------------------------------------------------------
        # xu ly bien nho:
##                if a6 > bien_nho_max:
##                    bien_nho_max = a6
        #        print("bien nho", a6)
        #---------------------------------------------------------------

                font = cv2.FONT_HERSHEY_SIMPLEX

#                frame2= cv2.putText(frame2, "xac suat nhan dan dung cua den:", (0,385),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
#                frame2= cv2.putText(frame2, str(int(a6)), (10,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)

#                frame2= cv2.putText(frame2, "(max", (40,410),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu

#                frame2= cv2.putText(frame2, str(int(bien_nho_max)), (100,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)
#                frame2= cv2.putText(frame2, ")", (130,410),font, 0.7, (0,0,255),2,cv2.LINE_AA)



                
                
                frame2= cv2.putText(frame2, "du lieu giai ma tu den:", (0,450),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
                frame2= cv2.putText(frame2, str(a8), (10,475),font, 0.7, (0,0,255),2,cv2.LINE_AA)

##                frame2= cv2.putText(frame2, "so anh da xu ly:", (450,450),font, 0.7, (0,0,255),2,cv2.LINE_AA) #1: co chu 1 : khoang cach chu, 1 do day chu
##                frame2= cv2.putText(frame2, str(bien_nho_so_anh), (460,475),font, 0.7, (0,0,255),2,cv2.LINE_AA)


            
            # convert it to texture
                buf1 = cv2.flip(frame2, 0)
                buf = buf1.tobytes()
                image_texture = Texture.create(
                    size=(frame2.shape[1], frame2.shape[0]), colorfmt='bgr')
                image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                # display image from the texture
                self.texture = image_texture


class CamApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_EXPOSURE, -14)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()
