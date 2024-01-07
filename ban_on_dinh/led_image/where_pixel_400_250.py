# Python program to explain cv2.circle() method 
    
# importing cv2 
import cv2 
    
# path 
path = "anh 1800_1001.jpg"
    
# Reading an image in default mode
image = cv2.imread(path)
    
# Window name in which image is displayed
window_name = 'Image'
   
# Center coordinates
center_coordinates = (330, 220) # width height
  
# Radius of circle
radius = 3
   
# Blue color in BGR
color = (0, 0, 255)
   
# Line thickness of 2 px
thickness = 2
   
# Using cv2.circle() method
# Draw a circle with blue line borders of thickness of 2 px
image = cv2.circle(image, center_coordinates, radius, color, thickness)
cv2.imwrite('anh_330_220'+'.jpg',image)   
# Displaying the image 
cv2.imshow(window_name, image) 
