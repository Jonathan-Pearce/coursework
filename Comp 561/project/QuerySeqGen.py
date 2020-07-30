from sys import stdin, stdout
import sys
import random
import math
import itertools
import Queue
from datetime import datetime
import os


basepairs = open('basepair.txt').readline()
probs = map(float, open('prob.txt').readline().split(' '))
print 'done reading file'

bpScore = {'A':0, 'C':1, 'G':2, 'T':3}
bps = ['A','C','G','T']
probscores = []

#fill probability matrix
########################################
for i in range(len(probs)):
	pos = bpScore[basepairs[i:i+1]]+1
	scores = [pos]
	score = probs[i]
	altScore = (1-score)/3
	for j in range(1,5):
		if j == pos:
			scores.append(score)
		else:
			scores.append(altScore)
	probscores.append(scores)
########################################

numSeq = 250
desiredLength = 1000
subRate = 0.20
indelRate = 0.20
seqSet = []

subCount = 0
inCount = 0

genomeLength = len(basepairs)

fileName = 'n=' + str(numSeq) + '_l=' + str(desiredLength) + '_sub=' + str(subRate) + '_indel=' + str(indelRate) + '.txt'
print fileName

#file = open(fileName, 'w+')

path = 'Input'
#file = open(os.path.join(path, fileName), 'w+')

with open(os.path.join(path, fileName), 'w+') as the_file:
    #the_file.write('Hello\n')

	#This will generate sequence
	for i in range(numSeq):
		seq = ''
		index = int(random.random() * (genomeLength-desiredLength))
		for j in range(index,index+desiredLength):
			rand = random.random()
			indexCount = 0
			for k in range(1,5):
				indexCount += probscores[j][k]
				if rand < indexCount:
					bpType = random.random()

					#substitution
					if bpType < subRate:
						sub = k
						while sub == k:
							sub = int(random.random()*4)+1
						seq += bps[sub-1]
						#print 'substitution'
						subCount += 1

					#inDel
					else:
						#insertion
						if bpType < subRate + indelRate/2:
							seq += bps[int(random.random()*4)]
							seq += bps[k-1]
							#print 'insertion'
							inCount += 1
						#deletion	
						elif bpType < subRate + indelRate and bpType > subRate + indelRate/2:
							randDel = random.random()
							while randDel < 0.8:
								#print 'deletion'
								j += 1
								randDel = random.random()
						else:
							seq += bps[k-1]
					break
		seqSet.append(seq)
		#print seq
		#print index
		if i != numSeq - 1:
			the_file.write(seq +' ' +str(index)+'\n')
		else:
			the_file.write(seq +' ' +str(index))

	#print subCount
	#print inCount
	#print seqSet
	sumset = 0

	#for i in seqSet:
	#	print len(i)
	#	sumset += len(i)

	print 1.0*sumset/numSeq






