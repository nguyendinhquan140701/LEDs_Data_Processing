import cv2
import numpy as np
import sys
img = cv2.imread("Encode_Decode/led_image/paper/paper_1_LED.png")


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.blur(gray, (5, 5), 0)
ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_EXTERNAL, 
                                    method=cv2.CHAIN_APPROX_NONE)
# draw contours on the original image

topmost1 = None
bottommost1 =None
contour_img = np.zeros_like(gray)
# loop the contours
for contourpy in contours:
    # get the topmost and bottommost points
    current_topmost = tuple(contourpy[contourpy[:, :, 1].argmin()][0])
    current_bottommost = tuple(contourpy[contourpy[:, :, 1].argmax()][0])

    # update the topmost and bottommost points
    if topmost1 is None or current_topmost[1] < topmost1[1]:
        topmost1 = current_topmost
        bottommost1 = current_bottommost

combined_contour = np.concatenate(contours)

# create the bounding convex hull
hull = cv2.convexHull(combined_contour)

P = topmost1
Q = bottommost1

cv2.putText(img, 'P', (P[0], P[1] - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
cv2.putText(img, 'Q', (Q[0], Q[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

# draw the convex hull
cv2.drawContours(img, [hull], -1, (0, 255, 0), thickness= 1)
cv2.imshow("Convex Hull Contour", img)
cv2.circle(img, topmost1, 3, (0, 0, 255), -1) # topmost point
cv2.circle(img, bottommost1, 3, (0, 0, 255), -1) # bottommost point

for contour in contours:
    # Get the bounding rectangle for each contour
    x, y, w, h = cv2.boundingRect(contour)

image_copy = img.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, 
                color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)


cv2.imshow("Image with Contour Lines", img)

cv2.imshow("Thresholded Image", thresh)

# Display the original image with contours
cv2.imshow("Contours", thresh)
cv2.imwrite("input_paper.png", thresh)

# Wait for a key press and close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()