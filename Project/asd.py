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
colors = ["pink", "blue", "dark blue", "green", "yellow","orange"]

for color in colors:
	counts[color] = 0

	#Define the ranges 
	if (color == "pink"):
		lower = np.array([128,7,252])
		upper = np.array([223,175,254])
	elif (color == "blue"):
		lower = np.array([195, 148, 13])
		upper = np.array([255, 238, 77])
	elif (color == "dark blue"):
		lower = np.array([229, 70, 20])
		upper = np.array([255, 166, 89])
	elif (color == "green"):
		lower = np.array([12, 182, 69])
		upper = np.array([66, 254, 189])
	elif (color == "yellow"):
		lower = np.array([51, 209, 239])
		upper = np.array([120, 252, 252])	
	elif (color == "orange"):
		lower = np.array([8, 63, 252])
		upper = np.array([84, 88, 255])

	#Create mask then apply it to the image to extract color
	mask = cv2.inRange(img, lower, upper)
	maskImg = cv2.bitwise_and(img, img, mask = mask)

	gray = cv2.cvtColor(maskImg, cv2.COLOR_BGR2GRAY)

	edge = cv2.Canny(gray, 100, 200)
	edge = cv2.dilate(edge, None, iterations = 1)

	(_, contours, _) = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	for c in contours:
		area = cv2.contourArea(c)
		#Change this to percentage/find a way tp use the largest one
		if (area < 1000):
			continue

		hull = cv2.convexHull(c)

		#Draw the contours. Not needed? For visuals only
		if (color == "pink"):
			cv2.drawContours(img, [hull], 0, (0, 0, 0))
		elif (color == "blue"):
			cv2.drawContours(img, [hull], 0, (0, 0, 0))
		elif (color == "dark blue"):
			cv2.drawContours(img, [hull], 0, (0, 0, 0))
		elif (color == "green"):
			cv2.drawContours(img, [hull], 0, (0, 0, 0))
		elif (color == "orange"):
			cv2.drawContours(img, [hull], 0, (0, 0, 0))
		elif (color == "yellow"):
			cv2.drawContours(img, [hull], 0, (0, 0, 0))

		counts[color] += 1
		total += 1
	#Tell user how many objects of that color
	print("{} {} object(s)".format(counts[color], color))

print("{} object(s) total".format(total))

cv2.imshow("asd", img)
key = cv2.waitKey(0)