import cv2
image = cv2.imread("anh 1800_1001.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


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







color = image[330, 220]
cv2.imwrite('anh_bao_contours'+'.jpg',image)
cv2.imshow("image", image)

# if image type is b g r, then b g r value will be displayed.
# if image is gray then color intensity will be displayed.
print(color)

# bin = 0
