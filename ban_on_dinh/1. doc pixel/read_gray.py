
import cv2
image = cv2.imread("anh 1800_1001.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
color = image[330, 220]
cv2.imwrite('anh_gray'+'.jpg',image) 
# if image type is b g r, then b g r value will be displayed.
# if image is gray then color intensity will be displayed.

print(color)
# [ 3  0 15]

# gray: 5
