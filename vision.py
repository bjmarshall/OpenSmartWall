import cv3
import numpy as np
import time

FPS = 24  #Change as desired
WAIT = int(1000 / FPS)

cap = cv3.VideoCapture(0)

time.sleep(3)

#Grab 30 images to get the camera adjusted and store a picture.
for dummy in range(200):
	ret, original = cap.read()

fgbg = cv3.createBackgroundSubtractorMOG()

grayOriginal = cv3.cvtColor(original, cv3.COLOR_BGR2GRAY)
original = cv3.flip(original, 1)

while True:
	ret, img = cap.read()	#capture image

	img = cv3.flip(img, 1)	#mirror image (for frontcams)
	
	#cv3.imshow('Original',img)

	gray = cv3.cvtColor(img, cv3.COLOR_BGR2GRAY)

	difference = fgbg.apply(img, learningRate=0.000)
	ret, thresh = cv3.threshold(difference, 200, 255, cv3.THRESH_BINARY)

	cv3.imshow('Original', original)
	cv3.imshow('Current', img)
	cv3.imshow('Difference', difference)
	cv3.imshow('Adjustment', thresh)

	
	difference2 = cv3.subtract(img, original)

	### Alter intensity
	phi = 1
	theta = 1
	maxIntensity = 255

	difference2 = (difference2**2)/255
	ret, difference2 = cv3.threshold(difference2, 1, 255, cv3.THRESH_BINARY)

	#cv3.imshow('Difference', difference)
	#cv3.imshow('Adjustment 1', difference1)
	#cv3.imshow('Adjustment 2', difference2)
	#cv3.imshow('Original', original)

	
	corners = cv3.goodFeaturesToTrack(gray, 100, 0.01, 10)
	corners = np.int0(corners)

	edges = cv3.Canny(gray,100,200)

	for i in corners:
	    x,y = i.ravel()
	    cv3.circle(img,(x,y),3,255,-1)	
	
	#cv3.imshow('Corners',img)
	#cv3.imshow('Edges', edges)
	k = cv3.waitKey(WAIT) & 0xff

	if k == 27:
		break

cap.release()
cv3.destroyAllWindows()