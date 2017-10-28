# import the necessary packages:
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui

# Opening an image and backing it up
I = cv2.imread("cups.jpg")
Original = I.copy()
# Creating a plain white image
WhiteImg = np.zeros(np.shape(I), np.uint8)
WhiteImg[:,:] = (255,255,255)

# #Convert to grayscale
G = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

#T, B = cv2.threshold(G, thresh = 250, maxval = 255, type = cv2.THRESH_BINARY + cv2.THRESH_OTSU)
B = cv2.adaptiveThreshold(G, maxValue = 255, adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType = cv2.THRESH_BINARY, blockSize = 21, C = 4)

# Remove noise
shape = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4))
opening = cv2.morphologyEx(B, cv2.MORPH_OPEN, shape)

# Find the background
bg = cv2.dilate(opening, shape)

# Find the foreground 
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
ret, fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)

# Finding unknown region
fg = np.uint8(fg)
unknown = cv2.subtract(bg, fg)

ret, markers = cv2.connectedComponents(fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers + 1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv2.watershed(I, markers)
WhiteImg[markers == -1] = [255,0,0]

cv2.imshow("t", WhiteImg)
key = cv2.waitKey(0)
#Thresholding image using adaptive thresholding. Constant offset is set to 3 as it gives a clearer result
# T = np.mean(G) + np.std(G)
# T = 200
# T, B = cv2.threshold(G, thresh = T, maxval = 255, type = cv2.THRESH_BINARY)

# #_, contours,_ = cv2.findContours(B, 1, 2)
# (_, cons, _) = cv2.findContours(B, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_SIMPLE)

# for cnt in cons:
# 	cv2.drawContours(I, [cnt], 0, (0,0,255), 1)

# # Use threshold to get the binary mask
# B = cv2.adaptiveThreshold(G, maxValue = 255, adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType = cv2.THRESH_BINARY, blockSize = 21, C = 5)

# # Clean up the region of interest (ROI) which is used to get the outlines of the objects.
# # Outline is taken to reduce noise in countours
# shape = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
# erosion = cv2.erode(B, shape)
# negErosion = 255 - erosion

# ROI = cv2.bitwise_and(I, I, mask = negErosion)
# WROI = cv2.bitwise_and(WhiteImg, WhiteImg, mask = erosion)

# combo = ROI + WROI

# gCombo = cv2.cvtColor(combo, cv2.COLOR_BGR2GRAY)
# # Create a new binary image for finding contours
# B2 = cv2.adaptiveThreshold(gCombo, maxValue = 255, adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType = cv2.THRESH_BINARY, blockSize = 21, C = 5)

# (_, cons, _) = cv2.findContours(B2, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_SIMPLE)

# for c in cons:
# 	# Get the contour perimeter
# 	peri = cv2.arcLength(c, False)
# 	# Approximate the polygonal curve
# 	approx = cv2.approxPolyDP(c, 0.02 * peri, False)

# 	# Get the area of the contour; this filters the smaller contours.
# 	area = cv2.contourArea(c)
# 	if area > 150:
# 		# Contour is drawn onto original image to see full effect of the contour
# 		cv2.drawContours(I, c, -1, (255, 0, 0), 2)