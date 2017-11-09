import numpy as np
import cv2

video = cv2.VideoCapture("Zorro.mp4")
# fps = int(video.get(cv2.CAP_PROP_FPS))
frameSize = (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# writer = cv2.VideoWriter("den.avi", -1, fps, frameSize)
cnt = 0
previous = None

def differences(img):
	# if previous is None:
	# 	previous = img

	#Get difference btwn previous frame & current frame
	diff = cv2.absdiff(previous, img)

	# Delta more than 
	thresh, binImg = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

	(_, conts, _) = cv2.findContours(binImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	# if len(conts) < 200 or len(conts) > 1000:
	# 	return img

	for c in conts:
		# Ignore contours that are too small or too big
		area = cv2.contourArea(c)
		if area < 10 or area > 100:
			continue
			
		# Boundary for box
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(WhiteImg, (x, y), (x+w, y+h), (0, 0, 0), -1)

	binMask = cv2.threshold(WhiteImg, 10, 255, cv2.THRESH_BINARY)[1]
	negBin = 255 - binMask

	painted = cv2.inpaint(img, negBin, 3, cv2.INPAINT_TELEA)

	# ROI = cv2.bitwise_and(previous, previous, mask = negBin)
	# otherROI = cv2.bitwise_and(img, img, mask = binMask)

	# newimg = ROI + otherROI

	# cv2.imshow("ROI", binMask)
	# cv2.waitKey(0)
	cv2.imwrite("painted_{}.jpg".format(cnt), painted)
	return painted

while cnt < 51:
	imgs = [video.read()[1] for i in range(5)]

	gray = [cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) for i in imgs]
	gray = [np.float64(i) for i in gray]

	noise = np.random.randn(*gray[1].shape)*10
	noisy = [i+noise for i in gray]
	noisy = [np.uint8(np.clip(i,0,255)) for i in noisy]
 
	WhiteImg = np.zeros(np.shape(imgs[1]), np.uint8)
	WhiteImg[:,:] = (255,255,255)
	WhiteImg = cv2.cvtColor(WhiteImg, cv2.COLOR_BGR2GRAY)

	denoise = cv2.fastNlMeansDenoisingMulti(noisy, imgToDenoiseIndex = 2, temporalWindowSize = 5, h = 4, templateWindowSize = 7, searchWindowSize = 21)
	
	# Sharpen
	kernel = np.array([[1,1,1], [1,1,1], [1,1,1]], dtype=float)/9
	kernImg = cv2.filter2D(denoise,ddepth=-1,kernel=kernel)
	
	if cnt == 0:
		previous = kernImg

	if cnt > 0 and cnt < 51:
		previous = differences(kernImg)

	# writer.write(denoise)
	# cv2.imwrite("mod_{}.jpg".format(cnt), denoise)

	frame_pos = video.get(cv2.CAP_PROP_POS_FRAMES)
	if frame_pos > 4:
		video.set(cv2.CAP_PROP_POS_FRAMES, frame_pos - 4)
	cnt += 1

video.release()
# writer.release()

	# kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]], dtype=float)
	# kernImg = cv2.filter2D(denoise,ddepth=-1,kernel=kernel)
	
	# cv2.imwrite("den_{}.jpg".format(cnt), kernImg)
    # cv2.imshow("denoise", denoise)
    # cv2.waitKey(0)