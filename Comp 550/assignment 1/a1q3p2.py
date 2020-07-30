#imports
import nltk
import string
import re
import io
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import KFold
from sklearn import model_selection
from sklearn import svm
from sklearn import linear_model
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#to ensure the same splits in cross validation 
random_seed = 7
pos = []
neg = []

stopwords = set(stopwords.words('english'))
includeStopWords = True

#Read files
positive = io.open('rt-polarity.pos', encoding = "ISO-8859-1")
negative = io.open('rt-polarity.neg', encoding = "ISO-8859-1")

#read and process positive segments
for line in positive:
	#remove punctuation
	lineClean = re.sub(r'['+string.punctuation+']+', ' ', line)
	#tokenize line
	words = word_tokenize(lineClean)		
	#include stop words
	if includeStopWords:
		sentiment = " ".join(words);
		pos.append(sentiment);
	#do not include stop words
	else:
		notStopWord = []
		for word in words:
			if word not in stopwords:
				notStopWord.append(word);
		sentiment = " ".join(notStopWord)
		pos.append(sentiment);

#read and process negative segments
for line in negative:
	#remove punctuation
	lineClean = re.sub(r'['+string.punctuation+']+', ' ', line)
	#tokenize line
	words = word_tokenize(lineClean)		
	#include stop words
	if includeStopWords:
		sentiment = " ".join(words);
		neg.append(sentiment);
	#do not include stop words
	else:
		notStopWord = []
		for word in words:
			if word not in stopwords:
				notStopWord.append(word);
		sentiment = " ".join(notStopWord)
		neg.append(sentiment);

#We now have our words with no punctuation (and no stop words)

#Divide data in train and test set
splitIndex = int((len(pos+neg)*.2)/2)

#only use for the final evaluation
testData = pos[0:splitIndex] + neg[0:splitIndex]
testLabels = [0]*splitIndex + [1]*splitIndex

#use for 5-fold cross validation
trainData = pos[splitIndex:] + neg[splitIndex:]
trainLabels = [0]*(len(trainData)/2) + [1]*(len(trainData)/2)

parameterTuning = True


if parameterTuning:
	#cv = CountVectorizer();
	cvData = CountVectorizer(ngram_range=(1, 2),min_df = 2,max_df=0.5);
	cvDataTransform = cvData.fit_transform(trainData);

	kf = KFold(n_splits=5, shuffle = True, random_state = random_seed);
	svm = svm.SVC(kernel='linear')
	log = linear_model.LogisticRegression()
	nb = MultinomialNB()

	for classifier in [svm,log, nb]:
		#decide on evaluation metric
		#accuracy, but can do confusion matrix to evaluate bias
		accuracy = model_selection.cross_val_score(classifier, cvDataTransform, trainLabels, cv=kf)
		print accuracy.mean()

#final model evaluation
else:
	cvData = CountVectorizer(ngram_range=(1, 2),min_df = 0.0,max_df=0.5);

	#have to transform data a whole
	dataTransform = cvData.fit_transform(testData+trainData);

	#split back into test and train
	testDataTransform = dataTransform[0:len(testData)]
	trainDataTransform = dataTransform[len(testData):]

	svm = svm.SVC(kernel='linear')
	log = linear_model.LogisticRegression()
	nb = MultinomialNB()

	#train the model with train data and train labels
	nb.fit(trainDataTransform, trainLabels)
	#test model with test data
	testPred = nb.predict(testDataTransform)
	#evaluate model with labels 
	print accuracy_score(testLabels, testPred)
	#confusion matrix
	print confusion_matrix(testLabels, testPred)

	#random predictor
	randPred = []
	for i in range(len(testPred)):
		if random.random() > 0.5:
			randPred.append(1)
		else:
			randPred.append(0)
	#accuracy of random predictor
	print accuracy_score(testLabels, randPred)