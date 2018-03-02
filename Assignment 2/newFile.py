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
#	This program functions with the following steps:																																																	
#	1. It prompts the user to select their desired video file.
#	2. It reads 5 frames from the video into an array. These frames will be used for denoising. If no frames are captured, the loop will be broken.
#	3. Convert all of the images to grayscale, then to float64. This is used to add noise in the next step.
#	4. A noise of variance 25 is then created and added to the captured frames. 
#	5. The noisy images are converted back to uint8 for processing.
#	6. A white image is created based on the size of one of the frames. This image will be used to create a mask in a later step.
#	7. The program will increment a count value for each frame that is processed. If the value is within the defined range of frames required, it will
#		perform processing on the frame. If not, the count will be incremented and the frame position will be moved back 4 places. Moving the position 
#		back 4 places enables a previously read frame to be read again. This is because once the video reader reads a frame, it will move on to the 
#		next frame and ignore the previous unprocessed frames. 
#	8. The fastNlMeansDenoisingMulti() function is used to denoise the frames. It uses 5 frames to denoise the third frame (output).
#	9. The pixels are averaged to reduce the remaining small-grain noise.
#	10. If there is no previous frame, set it to the averaged frame. The previous image is used to perform a delta with the current image in the next step. 
#	11. Once the difference is found, it is thresholded to create a binary image. This binary image is used to find contours. Contours that are too small
#		or large are ignored, and the remaining contours are drawn onto the white image and the original image.
#	12. The white image is used to create a binary mask, which is inverted to be able to use in the inpaint() function.
#	13. Inpaint() function is used to remove the detected changes by painting over it to match the neighborhood pixels.
#	14. The processed frame is written to the same directory as the selected video file. 
#
#	References:							
#	1. Stackoverflow.com. (2014). Python "SyntaxError: Non-ASCII character '\xe2' in file". [online] 
#		Available at: https://stackoverflow.com/questions/21639275/python-syntaxerror-non-ascii-character-xe2-in-file [Accessed 4 Oct. 2017].
#	2. Docs.opencv.org. (2017). Denoising — OpenCV 3.0.0-dev documentation. [online] 
#		Available at: https://docs.opencv.org/3.0-beta/modules/photo/doc/denoising.html [Accessed 9 Nov. 2017].	
#	3. Powell, V. (2014). Image Kernels explained visually. [online] setosa.io. Available at: http://setosa.io/ev/image-kernels/ [Accessed 9 Nov. 2017].
#	4. Stackoverflow.com. (2015). Getting movie properties with python and opencv. [online] 
#		Available at: https://stackoverflow.com/questions/27837981/getting-movie-properties-with-python-and-opencv [Accessed 9 Nov. 2017].	
#	5. Docs.opencv.org. (2017). Histograms - 2: Histogram Equalization. [online] 
#		Available at: https://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html [Accessed 9 Nov. 2017].
#	6. Stackoverflow.com. (2013). How to process images of a video, frame by frame in video streaming using Opencv python. [online] 
#		Available at: https://stackoverflow.com/questions/18954889/how-to-process-images-of-a-video-frame-by-frame-in-video-streaming-using-opencv [Accessed 9 Nov. 2017].
#	7. 	Docs.opencv.org. (2017). Image Denoising. [online] 
#		Available at: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_photo/py_non_local_means/py_non_local_means.html [Accessed 9 Nov. 2017].
#	8. Docs.opencv.org. (2016). Image Inpainting. [online] Available at: https://docs.opencv.org/3.2.0/df/d3d/tutorial_py_inpainting.html [Accessed 9 Nov. 2017].
#	9. ResearchGate. (2013). Why do we add Gaussian, speckle and additive noise to an image? What are the benefits of adding these types of noises to an image?. [online] 
#		Available at: https://www.researchgate.net/post/Why_do_we_add_Gaussian_speckle_and_additive_noise_to_an_image_What_are_the_benefits_of_adding_these_types_of_noises_to_an_image [Accessed 9 Nov. 2017].
#	10. Docs.opencv.org. (2015). Smoothing Images. [online] Available at: https://docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html [Accessed 9 Nov. 2017].
#
#	Performance:																																																								
#	1. The denoising function performs very slowly, which is why the output is 10 defined frames instead of a video file.
#	2. The program will only run as long as it has not reached the defined end frame.	
#	3. Noise is added because the denoising function will work better if there is a known noise. Please see Reference #9.														
#
#	Experiments:																							
#	1. To include links in this file, the first line had to be implemented. This solution was found online. Please see Reference #1.
#	2. The input file type was used as the output file type, but it could not find the library (for mp4 in the case of Zorro). This functionality was 
#		scrapped to prevent	compatibility issues.
#	3. Images without added noise was used, but found that the quality is worse. Noise is added to the image before processing.
#	4. The output looks better when the contours are drawn onto both the white image and the frame.
################################################################################################################################################################################################################################################
# Import the necessary packages:
import numpy as np
import cv2
from easygui import *

file = fileopenbox("Select a video.")
video = cv2.VideoCapture(file)
# fps = int(video.get(cv2.CAP_PROP_FPS))
# frameSize = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# writer = cv2.VideoWriter("den.avi", -1, fps, frameSize)
cnt = 0
previous = None
startFrame = 30
endFrame = 50

def differences(img):
	#Get difference btwn previous frame & current frame
	diff = cv2.absdiff(previous, img)

	# Delta more than 50
	thresh, binImg = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

	(_, conts, _) = cv2.findContours(binImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for c in conts:
		# Ignore contours that are too small or too big
		area = cv2.contourArea(c)
		if area < 10 or area > 100:
			continue
			
		# Boundary for box
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(WhiteImg, (x, y), (x+w, y+h), (0, 0, 0), -1)
		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), -1)

	binMask = cv2.threshold(WhiteImg, 10, 255, cv2.THRESH_BINARY)[1]
	negBin = 255 - binMask

	painted = cv2.inpaint(img, negBin, 1, cv2.INPAINT_NS)
	cv2.imwrite("final_{}.jpg".format(cnt), painted)
	return painted

while cnt <= endFrame:
	try: 
		# if cnt == video.get(cv2.CAP_PROP_FRAME_COUNT) - 4:
		# 	imgs = [video.read()[1] for i in range(4)]
		# else:
		imgs = [video.read()[1] for i in range(5)]
	except ValueError:
		False

	if cnt == 0 or cnt >= startFrame and cnt <= endFrame:
		gray = [cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) for i in imgs]
		gray = [np.float64(i) for i in gray]

		noise = np.random.randn(*gray[1].shape)*10
		noisy = [i+noise for i in gray]
		noisy = [np.uint8(np.clip(i,0,255)) for i in noisy]

		WhiteImg = np.zeros(np.shape(imgs[1]), np.uint8)
		WhiteImg[:,:] = (255,255,255)
		WhiteImg = cv2.cvtColor(WhiteImg, cv2.COLOR_BGR2GRAY)

		denoise = cv2.fastNlMeansDenoisingMulti(noisy, imgToDenoiseIndex = 2, temporalWindowSize = 5, h = 7, templateWindowSize = 7, searchWindowSize = 21)
		
		# Averaging pixels
		avg = cv2.blur(denoise, (5,5))

		if previous is None:
			previous = avg
		else:
			previous = differences(avg)

	# writer.write(denoise)

	frame_pos = video.get(cv2.CAP_PROP_POS_FRAMES)
	if frame_pos > 4:
		video.set(cv2.CAP_PROP_POS_FRAMES, frame_pos - 4)

	cnt += 1

video.release()
# writer.release()