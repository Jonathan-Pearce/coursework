import math
import glob
import sys
import argparse
import codecs
import argparse
import random
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

def processSentence(sentence):
    sentence = sentence.lower()  # put to lower case
    sentence = word_tokenize(sentence.strip())  # split by words
    sentence = pos_tag(sentence)

    newSentence = []

    for i in range(len(sentence)):
        #each element sentence[i] = (word,pos)
        pos = get_wordnet_pos(sentence[i][1])  # convert the POS tag
        if pos:
            newSentence.append(lmtzr.lemmatize(sentence[i][0], pos))
        else:  # if no conversion found, use default.
            newSentence.append(lmtzr.lemmatize(sentence[i][0]))
    
    newSentence = [w for w in newSentence if w not in stopwords.words('english') and not ispunct(w)]  # remove stop words and punctuation


    #print ' '.join(newSentence)

   	#join the words back together
   	#this is our processed sentence to return
    return ' '.join(newSentence)


def processFile(sentences):
	#format the sentences
    formatSentences = []
    for sentence in sentences:
        formatSentence = str(processSentence(sentence))
        formatSentences.append(formatSentence)

    #print formatSentences
    #print formatSentences[1]
    return formatSentences



def mergeFiles(articles):
	#create a list of all the sentences from the files
    sentences = []
    for article in articles:  # for each file,
        sentences = sentences + article
    return sentences

def ispunct(string):
    return not any(char.isalnum() for char in string)

#Source: https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def getWordProb(sentences):

    #print 'wordProbabilities'
    #print sentences

    wordProb = {}
    total = 0
    for sentence in sentences:  # for each sentence,
    	#get all the words
        words = sentence.split()  
		# for each word lemma, update count.
        for w in words:  
            total += 1
            if w in wordProb:
                wordProb[w] += 1
            else:
                wordProb[w] = 1
    
    for w in wordProb.keys():
        wordProb[w] /= (total*1.0)

    return wordProb


def getSentenceScores(sentences, wordProb):
	sentenceScores = []

	for sentence in sentences:
		words = sentence.split()
		length = len(words)
		score = 0
		
		for word in words:
			score += wordProb[word]
		
		score /= length
		sentenceScores.append(score)

	return sentenceScores


def sumbasic(articles, mode, rawText):
    #convert list of articles into one large list on sentences (processed and raw test)
    sentences = mergeFiles(articles)
    rawSentences = mergeFiles(rawText)

    #calculate word frequencies
    wordFreq = getWordProb(sentences)

    #calculate initial sentence scores
    sentence_scores = getSentenceScores(sentences, wordFreq)

    #print sentence_scores

    #print len(sentences)
    #print len(rawSentences)
    #print len(sentence_scores)

    #summary of articles
    summary = ""
    #length of summary
    length = 0
    #keep summary length below 100
    while length < 100:

    	#find word with highest frequency
    	bestWord = max(wordFreq, key=wordFreq.get)
        #print bestWord
        #print wordFreq[bestWord]

    	bestSentenceIndex = -1
    	bestSentenceScore = 0
    	#if we are in a mode that is not best-avg, we need to find the sentence with
        #the highest average probability that also contains the highest frequency word 
        if mode != "best-avg":
            for i in range(len(sentences)):
                #if the sentence contains the best word then check if it has the best score
                if bestWord in sentences[i]:
                    #print sentences[i]
                    #sentence i is eligble 
                    if sentence_scores[i] > bestSentenceScore:
                        bestSentenceIndex = i
                        bestSentenceScore = sentence_scores[i]
    	else:
            #if we're in best-avg then just pick the highest scoring sentence
    		bestSentenceIndex = sentence_scores.index(max(sentence_scores))

    	#At this point we have the sentence index of the sentence being added

    	#get raw sentence for summary
    	rawSummarySentence = rawSentences[bestSentenceIndex]
        #get processed sentence for updating word freq
        processedSummarySentence = sentences[bestSentenceIndex]

    	#add sentence, period and space to summary
    	summary += rawSummarySentence
    	summary += ' '
    	length += len(rawSummarySentence.split())


    	#we need to update probabilities
    	if mode != "simplified":
            words = processedSummarySentence.split(' ')
            for word in words:
                #for words in sentence square their frequency
                wordFreq[word] *= wordFreq[word]

    		#since word freq has changed we need to update sentence scores
    		sentence_scores = getSentenceScores(sentences, wordFreq)
        else:
            #if we're in simplified then just remove the best scoring sentence
            #remove the raw sentence as well
            #remove the sentence score too
            del sentences[bestSentenceIndex]
            del rawSentences[bestSentenceIndex]
            del sentence_scores[bestSentenceIndex]


    print summary


#working!
def leading(rawText):
    #print len(rawText)
    articleNum = int(random.random()*len(rawText))
    #print len(rawText[articleNum])
    article = rawText[articleNum]

    summary = ""
    length = 0
    sentenceNum = 0

    #build summary
    while length < 100:
        sentence = article[sentenceNum]
        sentenceNum += 1
        summary = summary + sentence
        summary += ' '
        length += len(sentence.split(' '))

    print summary


lmtzr = WordNetLemmatizer()

#read in articles
parse = argparse.ArgumentParser()
parse.add_argument("version",choices=("orig", "best-avg","simplified", "leading"))
parse.add_argument("cluster",nargs='+')
args = parse.parse_args()

originalSentences = []

formattedSentences = []  # list of dictionaries for each document.
for fileName in args.cluster:
    sentences = codecs.open(fileName, 'r', encoding='utf-8').read()
    sentences = codecs.encode(sentences, 'ascii', 'ignore')
    sentences = sent_tokenize(sentences)
    #raw sentences that we read
    originalSentences.append(sentences)
    #sentences after lower case, tokenization, lemmatization....
    formattedSentences.append(processFile(sentences))

version = args.version

if version == 'orig':
    sumbasic(formattedSentences, version, originalSentences)
elif version == 'best-avg':
    sumbasic(formattedSentences, version, originalSentences)
elif version == 'simplified':
    sumbasic(formattedSentences, version, originalSentences)
elif version == 'leading':
    leading(originalSentences)

