# import the necessary packages:
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui

video = cv2.VideoCapture("Zorro.mp4")
(check, I) = video.read()

i = 0

while check:
	cv2.imshow("frame", I)
	cv2.waitKey(1)
	if i < 10:
		f = print("Frame {} .jpg".format(i))
		cv2.imwrite(f, I)

	i = i + 1
	(check, I) = video.read()

video.release()