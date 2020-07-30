import sys
import math
import random

stepSize = 0.1

startingPoints = [0,1,2,3,4,5,6,7,8,9,10]
#startingPoints = [3]
temps = [5,500,50000]
cool = [0.5,0.75,0.9,0.99]

output = []

def function(x):
	if x >= 0 or x <= 10:
		return math.sin(x*x/2.0)/(math.log((x+4),2))
	else:
		return -1

startingPointList = []
for i in startingPoints: #cycle through starting points
	coolList = []
	for l in cool:
		tempList = []
		for k in temps:			
			alpha = l
			temp = k
			iterations = 0
			maxPos = i
			maxValue = function(i)
			pos = i
			value = function(i)

			moves = [-stepSize, stepSize]
			noChangeCount = 0

			while temp > 0.01 and noChangeCount < 10:

				newMoves = []

				for j in moves:
					curMove = pos + j
					#print curMove
					if curMove >= 0 and curMove <= 10:
						newMoves.append([function(curMove),curMove])
						#print value
						#print curValue


				randIndex = int(random.random()*len(newMoves))

				randNeighbourValue = newMoves[randIndex][0]
				randNeighbourPos = newMoves[randIndex][1]

				p = math.exp(-(value - randNeighbourValue)/temp)
				#print p
				#print temp

				#If best value yet, move there are update max stats
				if randNeighbourValue > maxValue:
					maxValue = randNeighbourValue
					maxPos = randNeighbourPos
					value = randNeighbourValue
					pos = randNeighbourPos
					noChangeCount = 0
					#betterSpot = True
				#If better than where we are currently, move 
				elif randNeighbourValue > value:
					value = randNeighbourValue
					pos = randNeighbourPos
					noChangeCount = 0
				#If not better, move with probability p = ...
				elif random.random() < p:
					value = randNeighbourValue
					pos = randNeighbourPos
					noChangeCount = 0
				else:
					noChangeCount += 1

				temp *= alpha
				iterations += 1

			#print 'final result' ,maxValue ,' at ',maxPos,' after ', iterations, ' iterations	'
			#print value
			tempList.append([maxPos,maxValue,iterations,l,k,i])
			#print coolList
		coolList.append(tempList)
	startingPointList.append(coolList)


#print startingPointList


#printing of data
indexOfPrint = [0,1,2]

for i in indexOfPrint:
	for j in startingPointList:
		for k in j:
			#print k 
			for l in k:
				print l[i],',',
		print j[0][0][5]
		#print '-1'
