from sys import stdin, stdout
import sys
import random
import math
import itertools
import Queue
from datetime import datetime
import time

print str(datetime.now())


def ExtendStage2(dataBaseIndex, queryIndex, direction):
	bpScore = {'A':0, 'C':1, 'G':2, 'T':3}
	bps = ['-','A','C','G','T']
	global seqLength, queryLength, probscores, query, stage3Rate

	indexDatabase = dataBaseIndex
	indexQuery = queryIndex
	direct = direction

	#how far to, if too big, scale it
	if direct == -1:
		lengthToEnd = min(indexQuery, indexDatabase)
	else:
		lengthToEnd = min(queryLength - indexQuery, seqLength - indexDatabase)
	if lengthToEnd > 100:
		lengthToEnd = 100

	#get section of query string
	if direct == -1:
		#if going to left, look behind us and then reverse strings
		queryString = query[indexQuery-lengthToEnd+2:indexQuery+2]
		basepairsString = basepairs[indexDatabase-lengthToEnd+2:indexDatabase+2]
		queryString = queryString[::-1]
		basepairsString = basepairsString[::-1]
	else:
		#going to the right, just look ahead
		queryString = query[indexQuery-1:indexQuery+lengthToEnd-1]
		basepairsString = basepairs[indexDatabase-1:indexDatabase+lengthToEnd-1]

	#print queryString
	#print basepairsString

	dp = [[0]*(lengthToEnd+1)]
	rowIndex = 1
	rowMax = 0
	rowMaxIndex = 0
	rowProp = 0


	while (rowIndex < 5 or stage3Rate < rowProp) and indexDatabase >= 0 and indexDatabase < seqLength and indexQuery >= 0 and indexQuery < queryLength and rowMaxIndex != lengthToEnd:
		newRow = [0]
		#bp type for entire row 
		elementChar = bps[probscores[indexDatabase][0]] #should be A,C,G,T

		for i in range(1,lengthToEnd+1):

			#figure out if it would be a match
			if elementChar == queryString[i-1:i]:
				match = 1
			else:
				match = 0

			newRow.append(max(newRow[i-1], dp[rowIndex-1][i-1]+match, dp[rowIndex-1][i]))

		#need this for proportion
		rowMax = max(newRow)
		rowMaxIndex = newRow.index(rowMax)
		dp.append(newRow)
		indexDatabase += direct
		indexQuery += direct
		rowProp = (1.0*rowMax)/rowIndex
		rowIndex += 1

	#print rowMax
	return rowMax


def ExtendStage1(dataBaseIndex, queryIndex,score, prob, natProb,currentCount,numMatches, direction):
	bpScore = {'A':0, 'C':1, 'G':2, 'T':3}
	bps = ['-','A','C','G','T']
	global seqLength, queryLength, probscores, query, w, stage2Rate

	indexDatabase = dataBaseIndex
	indexQuery = queryIndex
	seqProb = prob
	direct = direction
	seqScore = score
	prevScore = score
	seq2 = ''
	count = currentCount
	matches = numMatches
	smallCount = 0
	matchRate = stage2Rate #this is how strict your expansion will be
	localMaxIndex = [0,0]
	growing = True
	naturalProb = natProb #this should pretty much always be less that or equal to seqProb

	#stay within bounds of query and database
	while (smallCount < 5 or count*matchRate < numMatches) and indexDatabase >= 0 and indexDatabase < seqLength and indexQuery >= 0 and indexQuery < queryLength:
		element = probscores[indexDatabase][0] #indexDatabase of pMax
		char = query[indexQuery] #A,C,G,T

		#variable to help find local maximum
		prevScore = seqScore

		#if prob is 1.0 then take it for sure
		#do nothing to probalilty
		if probscores[indexDatabase][element] == 1.0:
			seq2 += bps[element] #take pMax
			if bps[element] == char:
				seqScore += 1
				numMatches += 1
			else:
				seqScore -= 1

		#if pMax is a match take it, greedy
		elif bps[element] == char:
			seq2 += bps[element] #take pMax
			seqProb *= probscores[indexDatabase][element]
			seqScore += 1
			numMatches += 1

		#otherwise, use probalistic approach
		#i.e. probably take pMax
		#but if not greedily take match
		else:
			rand = random.random()
			indexSum = 0

			for k in range(1,5):
				indexSum += probscores[indexDatabase][k]
				#found our spot
				if rand < indexSum:
					if element == k:
						seq2 += bps[element]
						seqProb *= probscores[indexDatabase][element]
						seqScore -= 1
					else:
						seq2 += char
						seqProb *= probscores[indexDatabase][k]
						seqScore += 1
						numMatches += 1
					break

		#calculate natural probability
		rand = random.random()
		indexSum = 0
		for k in range(1,5):
				indexSum += probscores[indexDatabase][k]
				#found our spot
				if rand < indexSum:
					naturalProb *= probscores[indexDatabase][k]
					break



		#keep track of previous local Maximum
		if seqScore > prevScore:
			growing = True
		else:
			if growing:
				localMaxIndex = [count, prevScore]
			growing = False

		indexDatabase += direct
		indexQuery += direct
		count += 1
		smallCount += 1

	#find last local maximum
	seq2 = seq2[0:localMaxIndex[0]]
	seqScore = localMaxIndex[1]
	count = localMaxIndex[0]


	if direct == 1:
		return seq2, seqScore, seqProb, naturalProb, count, numMatches
	else:
		#return string reversed
		return seq2[::-1], seqScore, seqProb, naturalProb, count, numMatches


#string of basepairs
basepairs = open('basepair.txt').readline()
#array of Pmax
probs = map(float, open('prob.txt').readline().split(' '))
#Query sequence
#query = open('sampled1000.txt').readline()
print 'done reading file'

#variables#############################
bpScore = {'A':0, 'C':1, 'G':2, 'T':3}
bps = ['A','C','G','T']
probscores = []
w = 9
 #key word length
seqLength = len(basepairs)
matchScore = 1
misMatchScore = -1
stage2Rate = 0.9
stage3Rate = 0.8
#######################################
print len(probs)
print len(basepairs)

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

#buidling seeds from database
#-ength w will mostly depend on size of database
########################################
seq = ''
prob = 1.0
seeds = {}
score = matchScore*w

for i in range(w):
	seq += basepairs[i:i+1]
	prob *= probs[i]
seeds[seq] = [[score, 0, prob]]

for i in range(1,seqLength-w+1):
	seq = seq[1:w]
	seq += basepairs[i+w-1:i+w]
	prob /= probs[i-1]
	prob *= probs[i+w-1]
	if seq in seeds:
		orgList = seeds.get(seq)
		orgList.append([score, i,prob])
		seeds[seq] = orgList
	else:
		seeds[seq] = [[score, i, prob]]
########################################


#measure time to do all sequences and then divide by size
start_time = time.time()
########################################################################################################################
########################################################################################################################
######################Everything from below here will be run for every sequence in txt file#############################
########################################################################################################################
########################################################################################################################
inputFile = 'n=250_l=1000_sub=0.15_indel=0.15'
#inputFile = 'sampled1000'
results = []
topScores = []
numAccurateSeedsArray = []
totalSeedsArray = []
#Query sequence
with open('Input/'+inputFile+'.txt') as f:
	for line in f:
		lineParts = line.split(' ')
		query = lineParts[0]
		correctIndex = int(lineParts[1])
		queryLength = len(query)
		numAccurateSeeds = 0
		totalSeeds = 0
		#print queryLength

		#Stage 2
		########################################
		hits = []
		for i in range(queryLength-w+1):
		#for i in range(500,530):
			#move through query sequence, looking at each section of length w
			querySeed = query[i:i+w]
			#print querySeed
			#print i

			if querySeed in seeds:
				seedSet = seeds[querySeed]
				#print seedSet
				ans = ''
				#go through each matching seed in database
				for j in range(len(seedSet)):
					totalSeeds+=1
					if seedSet[j][1] >= correctIndex and seedSet[j][1] <= correctIndex + queryLength:
						numAccurateSeeds += 1
					#extend left
					ans, newscore, newprob, expectedProb, newCount, newMatches = ExtendStage1(seedSet[j][1]-1,i-1,seedSet[j][0],seedSet[j][2], 1.0,w,w, -1)
					shiftLeft = len(ans)
					startIndex = seedSet[j][1] - shiftLeft
					#add seed
					ans += querySeed
					#extend right
					partialAns, score, probFinal, expectedProb, countFinal, matchesTotal = ExtendStage1(seedSet[j][1]+w,i+w,newscore,newprob, expectedProb,newCount,newMatches, 1)
					shiftRight = len(partialAns)
					ans += partialAns

					#extend Right stage 2

					if score > 0:
						hit = [score,seedSet[j][1]-i, seedSet[j][1], probFinal, seedSet[j][1]-shiftLeft-1,i-shiftLeft-1,seedSet[j][1]+shiftRight+w,i+shiftRight+w]
						hits.append(hit)
					#print hit
			else:
				continue

		#Stage 3
		########################################
		#sorts hits
		#take top 100 or whatever
		finalHits = []
		hits.sort()
		hitsSize = 100
		if len(hits) > hitsSize:
			hits = hits[len(hits)-hitsSize:]

		for i in range(len(hits)):
			#print 'After stage 1 score is: '+score
			newScore = hits[i][0]

			#extend Left stage 2
			extraScore = ExtendStage2(hits[i][4],hits[i][5],-1)
			newScore += extraScore
			#extend Right stage 2
			extraScore = ExtendStage2(hits[i][6],hits[i][7],1)
			newScore += extraScore

			finalHit = [newScore, hits[i][1], hits[i][2], hits[i][3]]
			finalHits.append(finalHit)

		#########################################
		#print len(hits)

		#percentile testing
		########################################

		#Output
		########################################
		finalHits.sort()
		size = len(finalHits)
		foundHit = False
		neighbourhood = 20
		numAccurateSeedsArray.append(numAccurateSeeds)
		totalSeedsArray.append(totalSeeds)
		
		for i in range(size):
			if i == 0:
				topScores.append(finalHits[size-1-i][0])
			if finalHits[size-1-i][2] >= correctIndex and finalHits[size-1-i][2] <= correctIndex + queryLength:
				results.append(i+1)
				foundHit = True
				break
		if not foundHit:
			results.append(0)
		if False:
			for i in range(5):
				print finalHits[size-1-i]
		########################################


########################################################################################################################
########################################################################################################################
######################Final output: variables, list of results, time, name of txt file used#############################
########################################################################################################################
########################################################################################################################
firstCount = 0
top5Count = 0
missCount = 0
rankOthers = []

for i in results:
	if i == 1:
		firstCount += 1
	elif i == 0:
		missCount += 1
	else:
		rankOthers.append(i+1)

	if i >= 1 and i <= 5:
		top5Count += 1



print inputFile
print 'seed size = ',w
print 'threshold 1 = ',stage2Rate
print 'threshold 2 = ',stage3Rate
#print 'neighbourhood = ', neighbourhood
print results
print("--- %s seconds ---" % (time.time() - start_time))
print 'Top hit rate: ',1.0*firstCount/len(results)
print 'Top 5 hit rate: ',1.0*top5Count/len(results)
print 'Miss rate: ',1.0*missCount/len(results)
if len(rankOthers) > 0:
	print 'average non 1 rank: ',1.0*sum(rankOthers)/len(rankOthers)
print 1.0*sum(topScores)/len(topScores)
print 1.0*sum(numAccurateSeedsArray)/len(numAccurateSeedsArray)
print 1.0*sum(totalSeedsArray)/len(totalSeedsArray)



