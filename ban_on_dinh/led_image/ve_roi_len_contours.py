import cv2
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



a, b = hc.check_roi_tu_arr(mass_centres_x, mass_centres_y, top, bot)
if a[0] == a[1] == a[2] == a[3] ==0 or abs(a[1]-a[3]>=480): #ok fix 480
    a = [0,0,0,103]
if b[0] == b[1] == b[2] == b[3] ==0 or abs(a[1]-a[3]>=480):
    b = [0,0,0,103]
#        print("roi1,roi2", a,b)

text1 = 'RoI'
#        text2 = 'r2'
x = width
image = hvr.ve_roi(image, text1, a, x) 







color = image[330, 220]
cv2.imwrite('anh_RoI_len_contours'+'.jpg',image)
cv2.imshow("image", image)

cv2.waitKey(0) # waits until a key is pressed
cv2.destroyAllWindows() # destroys the window showing image


# if image type is b g r, then b g r value will be displayed.
# if image is gray then color intensity will be displayed.
print(color)

# bin = 0
