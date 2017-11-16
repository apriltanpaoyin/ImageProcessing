# import the necessary packages:
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui
import math

# Opening an image and backing it up
img = cv2.imread("cups.jpg")
ori = img.copy()

counts = {}
total = 0
#Colours to look for
# red // orange // yellow // green // blue // dark blue // purple
colors = {"pink": [np.array([159,51,151]), np.array([248,185,255])], 
			"blue": [np.array([195, 148, 13]), np.array([255, 238, 77])], 
			"dark blue": [np.array([229, 70, 20]), np.array([255, 166, 89])],
			"green": [np.array([58, 101, 46]), np.array([122, 254, 142])],
			"yellow": [np.array([20, 186, 182]), np.array([111, 252, 255])],
			"orange": [np.array([8, 63, 252]), np.array([84, 88, 255])],
			"red" : [np.array([0, 0, 125]), np.array([185, 185, 255])],
			"purple": [np.array([73, 18, 54]), np.array([254, 131, 205])],
			"black": [np.array([21, 21, 21]), np.array([55, 55, 55])]}

keys = colors.keys()

for color in keys:
	counts[color] = 0

	#Create mask then apply it to the image to extract color
	lower = colors.get(color)[0]
	upper = colors.get(color)[1]
	mask = cv2.inRange(img, lower, upper)
	maskImg = cv2.bitwise_and(img, img, mask = mask)

	gray = cv2.cvtColor(maskImg, cv2.COLOR_BGR2GRAY)

	k = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], dtype=float)
	F = cv2.filter2D(gray, ddepth=-1, kernel=k)

	edge = cv2.Canny(F, 100, 200)
	edge = cv2.dilate(edge, None, iterations = 1)

	(_, contours, _) = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	area = []
	# Get area
	for c in contours:
		area.insert(0, cv2.contourArea(c))
	
	area = sorted(area, reverse=True)
	# contours = sorted(contours, key = cv2.contourArea, reverse = True)
	for c in contours:
		individual_area = cv2.contourArea(c)
		largest = area[0]
		# Change to ingnore area smaller than a certain size to count multiple objects?
		if (individual_area < largest):
			continue

		hull = cv2.convexHull(c)

		# Draw the contours. Not needed? For visuals only
		cv2.drawContours(img, [hull], 0, (0, 0, 0))

		counts[color] += 1
		total += 1
	# Tell user how many objects of that color
	print("{} {} object(s)".format(counts[color], color))

print("{} object(s) total".format(total))

cv2.imshow("asd", img)
key = cv2.waitKey(0)