from preprocessing import read_json_file, count_words, process_features, train_validate_test_split, text_length, stopWordFreq 
from linear_regression import least_squares
from descent import sgd, momentum, adam

import numpy as np

#Mean squared error
def MSE(X,y,w):
	predictions = np.matmul(X, w)
	error = np.matmul(np.transpose(y - predictions), y - predictions)/len(y)
	return error

#get the data file and process
data = read_json_file("../data/proj1_data.json")

#change number to determine of word feautures
#calculate most frequent words using only the training set
most_frequent_words = count_words([row["text"] for row in data[:10000]], 61)
#print(most_frequent_words)

#new custom feature
#get the length of each entry
length = text_length([row["text"] for row in data])

#new custom feature
#get the non stop word frequency from each entry
freq = stopWordFreq([row["text"] for row in data])

#build X and y matrices
X, y = process_features(data, length, freq,  most_frequent_words)

#partition data
train_X, train_y, validate_X, validate_y, test_X, test_y = train_validate_test_split(X, y)

#Experiments
##########################################################################################
#Code for 4 tasks involved in part 3 of the project
#change this variable to 1,2,3,4 depending on which task you want to work on
taskNum = 4

#run simple model with only 3 basic features
#closed form and gradient descent
if taskNum == 1:

	#just use 3 basic features and intercept term
	basicTrain_X = train_X[:,0:4]
	#train model via closed form solution
	basic_closedForm = least_squares(basicTrain_X, train_y)
	

	gradientMethod = 3

	if gradientMethod == 1:
		#run standard gradient descent
		weights = sgd(basicTrain_X,train_y)
	elif gradientMethod ==2:
		#run momentum gradient descent
		weights = momentum(basicTrain_X,train_y)
	else:
		#run adam gradient descent
		weights = adam(basicTrain_X,train_y)

	print basic_closedForm
	print weights

	print 'Closed Form training set MSE: ', MSE(basicTrain_X,train_y,basic_closedForm)
	print 'Closed Form validation set MSE: ',MSE(validate_X[:,0:4],validate_y,basic_closedForm)

	print 'Gradient Descent training set MSE: ', MSE(basicTrain_X,train_y,weights)
	print 'Gradient Descent validation set MSE: ', MSE(validate_X[:,0:4],validate_y,weights)

	#descentModel = sgd(basicTrain_X,train_y)

#Task 2 is done 
#run model with words feautures added to basic features
if taskNum == 2:

	#Task 3 Part 2 Code
	#Train and evaluate model with text features
	if True:
		#we have to remove the 2 custom features used later on from the dataset for these experiments
		textFeature_X = np.concatenate((train_X[:,0:4], train_X[:,6:]), axis=1)

		#train model via closed form solution
		closedForm = least_squares(textFeature_X, train_y)

		#remove the 2 custom features from the validation set as well!
		freqWordValidate_X = np.concatenate((validate_X[:,0:4],validate_X[:,6:]),axis=1)

		#calculate the training and validation of the model
		print 'Training set MSE: ', MSE(textFeature_X,train_y,closedForm)
		print 'Validation set MSE: ',MSE(freqWordValidate_X,validate_y,closedForm)

	#used this code to get the data for the figures
	else:
		index = 6
		maxIndex = len(X[0])
		for i in range(6,maxIndex+1):
			#take out the new features
			freqWordTrain_X = np.concatenate((train_X[:,0:4], train_X[:,6:i]), axis=1)
			#train model via closed form solution
			closedForm = least_squares(freqWordTrain_X, train_y)
			#remove the features from part 3 for the validation set
			freqWordValidate_X = np.concatenate((validate_X[:,0:4],validate_X[:,6:i]),axis=1)
			#print 'Training set MSE: ', MSE(freqWordTrain_X,train_y,closedForm)
			#print MSE(freqWordTrain_X,train_y,closedForm)
			#print 'Validation set MSE: ',MSE(freqWordValidate_X,validate_y,closedForm)
			print MSE(freqWordValidate_X,validate_y,closedForm)


		
#Task 3 is done 
#include custom features to model
if taskNum == 3:

	#concatenate allows us to decide which custom features to add
	#[0:5]+[6:] - only the first custom feature added to model
	#[0:4]+[5:] - only the second custom feature added to model
	#[0:4]+[4:] - both custom features added to model
	textFeature_X = np.concatenate((train_X[:,0:4], train_X[:,5:]), axis=1)
	freqWordValidate_X = np.concatenate((validate_X[:,0:4],validate_X[:,5:]),axis=1)

	#train model via closed form solution
	closedForm = least_squares(textFeature_X, train_y)

	#calculate the training and validation of the model
	print 'Training set MSE: ', MSE(textFeature_X,train_y,closedForm)
	print 'Validation set MSE: ',MSE(freqWordValidate_X,validate_y,closedForm)

#Task 4 is done
#This is the final evaluation using the test set
#just run with best model!
if taskNum == 4:
	#remove 1st custom feature to avoid overfitting
	textFeature_X = np.concatenate((train_X[:,0:4], train_X[:,5:]), axis=1)
	closedForm = least_squares(textFeature_X, train_y)

	#remove 1st custom feature from validate and test set as well
	freqWordValidate_X = np.concatenate((validate_X[:,0:4],validate_X[:,5:]),axis=1)
	testX = np.concatenate((test_X[:,0:4],test_X[:,5:]),axis=1)

	print 'Training set MSE: ', MSE(textFeature_X,train_y,closedForm)
	print 'Validation set MSE: ', MSE(freqWordValidate_X,validate_y,closedForm)
	print 'Test set MSE: ', MSE(testX,test_y,closedForm)


