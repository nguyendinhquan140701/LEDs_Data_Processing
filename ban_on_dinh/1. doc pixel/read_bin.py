import cv2
image = cv2.imread("anh 1800_1001.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, image = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)
color = image[330, 220]
cv2.imwrite('anh_bin'+'.jpg',image)
cv2.imshow("image", image)
# if image type is b g r, then b g r value will be displayed.
# if image is gray then color intensity will be displayed.
print(color)

# bin = 0
