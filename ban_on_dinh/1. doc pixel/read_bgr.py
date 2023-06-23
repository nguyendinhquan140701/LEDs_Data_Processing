
import cv2
image = cv2.imread("anh 1800_1001.jpg")
color = image[330, 220]
# if image type is b g r, then b g r value will be displayed.
# if image is gray then color intensity will be displayed.
print(color)
# [ 3  0 15]
