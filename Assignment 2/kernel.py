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

def differences(previous, img, cnt):
	# if previous is None:
	# 	previous = img

	#Get difference btwn first frame & current frame
	diff = cv2.absdiff(previous, img)

	# Delta more than 110
	thresh, binImg = cv2.threshold(diff, 110, 255, cv2.THRESH_BINARY)
	negBin = 255 - binImg
    
	ROI = cv2.bitwise_and(previous, previous, mask = negBin)
	otherROI = cv2.bitwise_and(img, img, mask = binImg)
    
	img = ROI + otherROI

	cv2.imwrite("mod_{}.jpg".format(cnt), img)

def processFrame(cnt, img):
	# if cnt == 150:
	# 	cv2.imwrite("ori_150.jpg", img)

	# Add edges to the image to make the edges sharper?

	if cnt > 48 and cnt < 69 :
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		# Sharpen
		kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]], dtype=float)
		kernImg = cv2.filter2D(img,ddepth=-1,kernel=kernel)

		denoise = cv2.fastNlMeansDenoising(kernImg,None,7,7,21)

		clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2,2))
		claImg = clahe.apply(denoise)

		# smooth = cv2.GaussianBlur(claImg,(5,5),0)
		return cnt, claImg
	else:
		return cnt, img

while True:
	(grabbed, img) = video.read()
	cnt += 1

	#if can't grab frame
	if not grabbed:
		break

	cnt, processed = processFrame(cnt, img)

	if cnt == 49:
		previous = processed

	if cnt > 49 and cnt < 69:
		differences(previous, processed, cnt)
	
	# writer.write(smooth)

video.release()
# writer.release()
cv2.destroyAllWindows()