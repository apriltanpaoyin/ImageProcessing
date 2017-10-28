# import the necessary packages
import numpy as np
import argparse
import cv2
import easygui

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
# Opening an image using a File Open dialog:
img = cv2.imread("cups.jpg")

# Creating a plain white image
WhiteImg = np.zeros(np.shape(img), np.uint8)
WhiteImg[:,:] = (255,255,255)

HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#G = cv2.cvtColor(HSV,cv2.COLOR_BGR2GRAY)

k = np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-1]],
dtype=float)
F = cv2.filter2D(img,ddepth=-1,kernel=k)
G = cv2.cvtColor(F,cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(G,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
 
# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

#Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

#Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

markers = cv2.watershed(img,markers)
WhiteImg[markers == -1] = [255,0,0]

cv2.imshow("t", img)
key = cv2.waitKey(0)