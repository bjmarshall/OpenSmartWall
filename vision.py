import cv2
import numpy as np
import time

FPS = 24  #Change as desired
WAIT = int(1000 / FPS)

cap = cv2.VideoCapture(0)

time.sleep(3)

#Grab 30 images to get the camera adjusted and store a picture.
for dummy in range(30):
	ret, original = cap.read()

fgbg = cv2.createBackgroundSubtractorMOG2()

grayOriginal = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
original = cv2.flip(original, 1)

while True:
	ret, img = cap.read()	#capture image

	img = cv2.flip(img, 1)	#mirror image (for frontcams)
	
	#cv2.imshow('Original',img)

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	difference = fgbg.apply(img, learningRate=0.000)
	ret, thresh = cv2.threshold(difference, 200, 255, cv2.THRESH_BINARY)

	cv2.imshow('Original', original)
	cv2.imshow('Current', img)
	cv2.imshow('Difference', difference)
	cv2.imshow('Adjustment', thresh)

	
	difference2 = cv2.subtract(img, original)

	### Alter intensity
	phi = 1
	theta = 1
	maxIntensity = 255

	difference2 = (difference2**2)/255
	ret, difference2 = cv2.threshold(difference2, 1, 255, cv2.THRESH_BINARY)

	#cv2.imshow('Difference', difference)
	#cv2.imshow('Adjustment 1', difference1)
	#cv2.imshow('Adjustment 2', difference2)
	#cv2.imshow('Original', original)

	
	corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
	corners = np.int0(corners)

	edges = cv2.Canny(gray,100,200)

	for i in corners:
	    x,y = i.ravel()
	    cv2.circle(img,(x,y),3,255,-1)	
	
	#cv2.imshow('Corners',img)
	#cv2.imshow('Edges', edges)
	k = cv2.waitKey(WAIT) & 0xff

	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()