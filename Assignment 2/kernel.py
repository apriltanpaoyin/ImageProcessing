# -*- coding: utf-8 -*-
################################################################################################################################################################################################################################################
#
#	(C) Pao Yin Tan 2017	   																																																					
#
#	Student Name: (April) Pao Yin Tan 																																																			
#	Student No: D14124009		   																																																				
#	Course: 	DT211C			   																																																				
#	Date:		30/10/17			   																																																				
#	Title:		Assignment 2																																																					
#	Introduction:																																																								
#	This is a program that cleans up a clip from an old black-and-white movie.																																								
#
#	This program has the following functions:																																																	
#
#
#	References:							
#	1. Stackoverflow.com. (2014). Python "SyntaxError: Non-ASCII character '\xe2' in file". [online] Available at: https://stackoverflow.com/questions/21639275/python-syntaxerror-non-ascii-character-xe2-in-file [Accessed 4 Oct. 2017].																			
#
#	Performance:																																																								
#	1. Suuuuuuper slow cause of denoising																							
#
#	Experiments:																							
#	1. To include links in this file, the first line had to be implemented. This solution was found online. Please see Reference #1.
#	2. Tried to use the input file type as the output file type, but it could not find the library (for mp4 in the case of Zorro). 
#		Decided to scrap to prevent	compatibility issues.
################################################################################################################################################################################################################################################
# Import the necessary packages:
import numpy as np
import cv2

video = cv2.VideoCapture("Zorro.mp4")
# Params needed for video writer
# fourcc = int(video.get(cv2.CAP_PROP_FOURCC))
# fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fps = int(video.get(cv2.CAP_PROP_FPS))
frameSize = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Define video writer to writea new video
# writer = cv2.VideoWriter("output.avi", fourcc, fps, frameSize)
# writer = cv2.VideoWriter("output.avi", -1, fps, frameSize)
cnt = 0
# First frame
previous = None
WhiteImg = None

def differences(previous, img, cnt):
	# if previous is None:
	# 	previous = img

	#Get difference btwn previous frame & current frame
	diff = cv2.absdiff(previous, img)

	# Delta more than 
	thresh, binImg = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
	# binImg = cv2.dilate(binImg, None, iterations = 2)
	# negBin = 255 - binImg

	(_, cnts, _) = cv2.findContours(binImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
    
	# ROI = cv2.bitwise_and(previous, previous, mask = negBin)
	# otherROI = cv2.bitwise_and(img, img, mask = binImg)

	# newimg = ROI + otherROI

	for c in cnts:
		# Ignore contours that are too small
		if cv2.contourArea(c) > 100:
			continue
			
		# Boundary for box
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(WhiteImg, (x, y), (x+w, y+h), (0, 0, 0), -1)

	binMask = cv2.threshold(WhiteImg, 10, 255, cv2.THRESH_BINARY)[1]
	negBin = 255 - binMask

	ROI = cv2.bitwise_and(previous, previous, mask = negBin)
	otherROI = cv2.bitwise_and(img, img, mask = binMask)

	newimg = ROI + otherROI

	# cv2.imshow("ROI", newimg)
	# cv2.waitKey(0)
	cv2.imwrite("mod_{}.jpg".format(cnt), newimg)
	return img

def processFrame(img):
	# if cnt == 150:
	# 	cv2.imwrite("ori_150.jpg", img)

	# Add edges to the image to make the edges sharper?

	if cnt > 103 and cnt < 116 :
		if len(img.shape) > 2:
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Sharpen
		kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]], dtype=float)
		kernImg = cv2.filter2D(img,ddepth=-1,kernel=kernel)

		denoise = cv2.fastNlMeansDenoising(kernImg,None,7,7,21)

		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2,2))
		claImg = clahe.apply(denoise)

		# smooth = cv2.GaussianBlur(claImg,(5,5),0)
		return claImg
	else:
		return img

while True:
	(grabbed, img) = video.read()
	cnt += 1

	#if can't grab frame
	if not grabbed:
		break

	processed = processFrame(img)

	WhiteImg = np.zeros(np.shape(img), np.uint8)
	WhiteImg[:,:] = (255,255,255)
	WhiteImg = cv2.cvtColor(WhiteImg, cv2.COLOR_BGR2GRAY)

	if cnt == 104:
		previous = processed

	if cnt > 104 and cnt < 116:
		previous = differences(previous, processed, cnt)
	
	# writer.write(again)

video.release()
# writer.release()
cv2.destroyAllWindows()