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
writer = cv2.VideoWriter("output.avi", -1, fps, frameSize)
cnt = 0

def processFrame(cnt, img):
	# if cnt == 150:
	# 	cv2.imwrite("ori_150.jpg", img)
	# if cnt == 600:
	# 	cv2.imwrite("ori_600.jpg", img)

	# Add edges to the image to make the edges sharper?

	# if cnt == 650:
	denoise = cv2.fastNlMeansDenoising(img,None,7,7,21)

	denoise = cv2.cvtColor(denoise, cv2.COLOR_BGR2GRAY)

	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2,2))
	cla = clahe.apply(denoise)

	# Sharpen
	kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]], dtype=float)
	kernImg = cv2.filter2D(denoise,ddepth=-1,kernel=kernel)

	# Gaussian from notes
	kernel = np.array([[1,4,1], [4,7,4], [1,4,1]], dtype=float)/27
	smooth = cv2.filter2D(kernImg,ddepth=-1,kernel=kernel)

		# cv2.imshow("cla", cla)
		# cv2.imshow("smooth", smooth)
		# key = cv2.waitKey(0)

		# cv2.imwrite("mod_{}.jpg".format(cnt), smooth)
	# if cnt == 600:
	# 	denoise = cv2.fastNlMeansDenoising(img,None,7,7,21)

	# 	kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]], dtype=float)
	# 	kernImg = cv2.filter2D(denoise,ddepth=-1,kernel=kernel)

	# 	cv2.imwrite("mod_600.jpg", kernImg)
	return smooth

while True:
	(grabbed, img) = video.read()
	cnt += 1

	#if can't grab frame
	if not grabbed:
		break
	else:
		smooth = processFrame(cnt, img)
		print cnt
		writer.write(smooth)

	
video.release()
# writer.release()
cv2.destroyAllWindows()