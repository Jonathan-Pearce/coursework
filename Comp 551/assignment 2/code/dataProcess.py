import os
import re
import string
import glob
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
#list of stop words
stop_words = set(stopwords.words('english'))

#Boolean to keep or remove stop words
removeStopWords = True

#Boolean to determine whether we are just making a sample file
#Only set to true if you want to check that your code/file is building properly
sample = True

#name of file we are writing the text data into
#try to make it descriptive - i.e. whether its the pos, neg or test set and what kind of processing was done
file = open('data_withstopwords.pos','w')

#helps estimate how many files have been processed
index = 0

# we need to lematize the words
lematizer = nltk.WordNetLemmatizer()
#iterate through directory
#either 'train/pos' or 'train/neg' or 'test'
for filename in glob.glob(os.path.join('test', '*.txt')):

	#for keeping track of progress
	if index % 100 == 0:
		print(index)

	if sample:
		if index == 1000:
			file.close
			sys.exit(0)

	#print(filename)

	#read current file
	with open(filename) as f:
		#get text
		content = f.readline()
		#clean up text
		content = content.strip() 
		lineClean = re.sub(r'['+string.punctuation+']+', '', content)
		#to lower case
		lineLower = lineClean.lower()

		#Remove stop words if we want
		if removeStopWords:
			#tokenize line
			raw_words = word_tokenize(lineLower)
			words = [lematizer.lemmatize(w.lower()) for w in raw_words if w.isalpha() and w not in stop_words]
			#print(words)
			text =  " ".join(words);

		else:
			text = lineLower

		#append text to file
		file.write(text+'\n')
		index += 1

#close file
file.close()
