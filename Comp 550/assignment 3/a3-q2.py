import loader
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.wsd import lesk
import string
from nltk.stem.wordnet import WordNetLemmatizer
import math
import sys

#remove stop words
def remove_stopwords(s):
	for item in s.values():
		#for word in item.context:
		filtered_words = [word for word in item.context if word not in stopwords.words('english')]
			#if word in stopwords.words('english'):
			#	print wordc
			#	item.context.remove(word)

		item.context = filtered_words
		#print item.context

#remove punctuation
def remove_punc(s):
	for item in s.values():
		removeWords =  [i for i in item.context if all(j.isdigit() or j in string.punctuation for j in i)]
		for i in removeWords:
			item.context.remove(i)


#change underscore to space
def change_underscore(s):
	for item in s.values():
		for word in item.context:
			word.replace('_', ' ')

#lemmatize words
def lemmatize(s):
	lmtzr = WordNetLemmatizer()
	for item in s.values():
		newWords = []
		#print 'old: ',item.context
		for word in item.context:
			newWords.append(lmtzr.lemmatize(word))
			#item.context.remove(word)
			#item
		#print 'new: ',newWords

		item.context = newWords

#length of context
def contextLength(s):
	size = len(s)
	total = 0

	for entry in s:
		total += len(s[entry].context)

	print total*1.0/size

#number of senses
def numberOfSenses(s):
	size = len(s)
	total = 0

	for entry in s:
		word = s[entry].lemma

		total += len(wn.synsets(word))

		if len(wn.synsets(word)) == 0:
			print 'zero'
			print word

	print total*1.0/size



#Baseline
def baseline(s, k):
	total=0
	count=len(s)
	for entry in s:
		word=s[entry].lemma
		#get first synset
		m=wn.synsets(word)[0]
		
		for key in k[entry]:
			#if wn.synset_from_sense_key(key) == result:
			if wn.lemma_from_key(key).synset() == m:
				total+=1

	print 'baseline accuracy: ',float(total)/count

#NLTK Lesk
def leskAlg(s, k):

	correct = [0]*100
	incorrect = [0]*100

	total=0
	count=len(s)
	for entry in s:
		x=[]
		result=(lesk(s[entry].context, s[entry].lemma))#.lemmas()

		correctCheck = False

		for key in k[entry]:
			#if wn.synset_from_sense_key(key) == result:
			if wn.lemma_from_key(key).synset() == result:
				correctCheck = True

				total+=1

				word = s[entry].lemma

				correct[len(wn.synsets(word))] += 1
				#correct[0] += 1

		if not correctCheck:
			word = s[entry].lemma

			incorrect[len(wn.synsets(word))] += 1
			#incorrect[0] += 1 

	print correct
	print incorrect
	print (sum(correct) + sum(incorrect))
		#break
	lesk_accuracy = float(total)/count
	print "Lesk accuracy: ",lesk_accuracy

#intersection of two lists
def intersection(lst1, lst2): 
	lmtzr = WordNetLemmatizer()
	#lemmatize word sense definition
	a = [x.lower() for x in lst1]

	
	newWords = []

	for word in lst2:
		newWords.append(lmtzr.lemmatize(word))
		#item.context.remove(word)
		#item

	b = [x.lower() for x in newWords]

	lst3 = [value for value in a if value in b] 
	#print len(lst3)
	return lst3 


#Model 3
def leskAlgDist(s,k):

	overlapTotal = [0]*50

	total = 0
	count = len(s) #number of cases to solve

	for entry in s:
		#get lemma
		word=s[entry].lemma
		#print word

		#words in context
		lemmaContext = s[entry].context

		#iterate through senses of the lemma
		rank = 0
		alpha = 6
		bestScore = 0
		sense = None
		length = len(wn.synsets(word))

		#print length

		for ss in wn.synsets(word):
			#rank tells us how frequently this sense is used
			rank += 1 
			rankScore = alpha*(length - rank + 1)

			#words in sense
			senseDef = ss.definition().split(' ')

			#overlap score
			overlap = len(intersection(lemmaContext, senseDef))

			overlapTotal[overlap] += 1

			#smooth values in case all are 0
			overlap += 1

			#overlap = 0
			#overlap /= 2.0
			#overlap = math.pow(2,overlap)

			finalScore = overlap + rankScore
			#print finalScore

			if finalScore > bestScore:
				bestScore = finalScore
				sense = ss


		#print sense
		#print sense.lemmas()

		x=[]
		#for item in sense.lemmas()[0]:
			#print item
			#x.append(item.key().encode("utf-8"))

		#x = (sense.lemmas()[0]).key().encode("utf-8")

		#for key in k[entry]:
		#	if key in x:
		#		total+=1


		for key in k[entry]:
			#if wn.synset_from_sense_key(key) == result:
			if wn.lemma_from_key(key).synset() == sense:
				total+=1

		#break
	print overlapTotal
	print total/(count*1.0)


#MODEL 4
def smartLesk(s,k,wordRank):
	total = 0
	count = len(s) #number of cases to solve

	for entry in s:

		word=s[entry].lemma
		#print word

		#words in context
		lemmaContext = s[entry].context

		#iterate through senses of the lemma
		bestScore = -1
		sense = wn.synsets(word)[0]

		#print length

		for ss in wn.synsets(word):			
			#words in sense
			senseDef = ss.definition().split(' ')
			#list of overlap words
			overlap = intersection(lemmaContext, senseDef)

			score = 0
			for i in overlap:
				#find rank
				#if i in dataset
				#score will increase by 1 - 1/rank
				if i in wordRank:
					#more common words are not as important and telling
					rankScore = 1 - (1.0/math.log10(wordRank.index(i)))
					#print wordRank.index(i)
					#print i
					#print rankScore
					#sys.exit(0)
				else:
					#if its an uncommon word, score will go up by 1
					rankScore = 1

				#print i
				#print rankScore

				score += rankScore

			if score > bestScore:
				bestScore = score
				sense = ss

		

		for key in k[entry]:
			#print word
			#print sense
			#print wn.lemma_from_key(key).synset()
			#if wn.synset_from_sense_key(key) == result:
			if wn.lemma_from_key(key).synset() == sense:
				total+=1


	print total/(count*1.0)




#read data
data_f = 'multilingual-all-words.en.xml'
key_f = 'wordnet.en.key'
dev_instances, test_instances = loader.load_instances(data_f)
dev_key, test_key = loader.load_key(key_f)

#correct entries
# IMPORTANT: keys contain fewer entries than the instances; need to remove them
dev_instances = {k:v for (k,v) in dev_instances.iteritems() if k in dev_key}
test_instances = {k:v for (k,v) in test_instances.iteritems() if k in test_key}


remove_stopwords(test_instances)
#sys.exit(0)
remove_punc(test_instances)
change_underscore(test_instances)
#lowercase(test_instances)
lemmatize(test_instances)

#print dev_key
#sys.exit(0)


#print len(dev_instances)
#print len(dev_key)
#print len(test_instances)
#print len(test_key)


contextLength(test_instances)
#numberOfSenses(test_instances)
sys.exit(0)

#print len(test_instances)
#print dev_instances
#print dev_instances

#print len(dev_key)
#print dev_key


#run models
baseline(test_instances,test_key)
leskAlg(test_instances,test_key)
#leskAlgDist(dev_instances, dev_key)
leskAlgDist(test_instances, test_key)
#sys.exit(0)

#final method

#build word rank list
size = 1000

wordsRank = [0]*(size+1)

#read external lexical resource
import csv
with open('unigram_freq.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for i,row in enumerate(reader):
        #print row['word']
        #print i
        wordsRank[i] = row['word']
        if(i >= size):
            break

#print wordsRank

#model #4
smartLesk(test_instances, test_key,wordsRank)


