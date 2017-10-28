# import the necessary packages:
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui
import math

# Opening an image and backing it up
I = cv2.imread("cups.jpg")
Original = I.copy()

# #Convert to grayscale
G = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

Ix = cv2.Sobel(G, ddepth=cv2.CV_64F, dx=1, dy=0)
Iy = cv2.Sobel(G, ddepth=cv2.CV_64F, dx=0, dy=1)

#mag = np.hypot(Ix, Iy)
mag = np.sqrt(Ix**2, Iy**2)
#mag = cv2.Sobel(G, ddepth=cv2.CV_64F, dx=1, dy=1)

E = cv2.Canny(G, threshold1=100, threshold2=200)

#Put edge mask on gradient magnitude
gradientEdge = cv2.bitwise_and(mag, mag, mask = E)

#plt.imshow(E, cmap='gray')
plt.imshow(gradientEdge, cmap='gray')
plt.show()
#cv2.imshow("asd", gradientEdge)
key = cv2.waitKey(0)