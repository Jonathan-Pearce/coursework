import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import cv2
import matplotlib.pyplot as plt
import pickle


#size of outputted images
imSize = 28
#used for pixel value thresholding
maxValue = 250

train = True

if train:
	images = pd.read_pickle('input/train_images.pkl')
	train_labels = pd.read_csv('input/train_labels.csv')
else:
	images = pd.read_pickle('input/test_images.pkl')
	#numpy array for new cropped images
	output = np.zeros(shape=(len(images),imSize,imSize))

#testIndex = 17
#print(train_images.shape[0])
#print(len(train_images))
#plt.title('Label: {}'.format(train_labels.iloc[testIndex]['Category']))
#plt.imshow(images[testIndex])
#plt.show()

#number of poorly processed images
count = 0

#numpy array for new cropped images
output = np.zeros(shape=(len(images),imSize,imSize))
print(output.shape)

for i in range(len(output)):
#for i in range(testIndex,testIndex+1):

	#get image i
	img = images[i]

	#convert to correct data type
	imgFloat = img.astype(np.uint8)

	#filter image
	(ret,thresh) = cv2.threshold(imgFloat,maxValue,255,0)

	#get countours
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#find largest bounding box that is not larger than 28x28
	#largest bounding box is considered a square so examine maximum of width and height
	maxDim = -1
	maxIndex = -1

	for j in range(len(contours)):
		cnt = contours[j]

		x,y,w,h = cv2.boundingRect(cnt)

		#print(w)
		#print(h)
		#print(x)
		#print(y)

		if max(w,h) > maxDim and max(w,h) <= 28:
			maxIndex = j
			maxDim = max(w,h)

	#print(maxDim)
	#print(maxIndex)

	#get bounding box for largest digit

	#image only has bounding boxes greater than desired size
	#just use the first bounding box

	#only ~30 images fall here so not a huge deal
	if maxIndex == -1:
		x,y,w,h = cv2.boundingRect(contours[0])
		#concatenate bounding box
		w = min(w,imSize)
		h = min(h,imSize)
		count += 1
		#print('here')

	else:
		x,y,w,h = cv2.boundingRect(contours[maxIndex])

	
	#get bounding box number
	boundingBox = thresh[y:y+h,x:x+w]

	#plt.imshow(boundingBox)
	#plt.show()
	#sys.exit(0)

	#At this point we have the bounding box of the largest digit
	#and the dimension do not exceed 28x28

	#create blank image
	imCrop = np.zeros(shape=(imSize,imSize))

	offsetX = int((imSize - w)/2.0)
	offsetY = int((imSize - h)/2.0)

	imCrop[offsetY:h+offsetY,offsetX:w+offsetX] = boundingBox

	#plt.imshow(imCrop)
	#plt.show()
	#sys.exit(0)

	output[i] = imCrop

#print(count)
#print(output.shape)

#sys.exit(0)

#writing files
if train:
	pickling_on = open("trainCrop.pkl","wb")
else:
	pickling_on = open("testCrop.pkl","wb")

pickle.dump(output, pickling_on)
pickling_on.close()

