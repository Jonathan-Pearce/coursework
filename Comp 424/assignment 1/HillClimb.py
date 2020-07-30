import sys
import math

stepSize = 0.00

startingPoints = [0,1,2,3,4,5,6,7,8,9,10]
#startingPoints = [3]

def function(x):
	if x >= 0 or x <= 10:
		return math.sin(x*x/2.0)/(math.log((x+4),2))
	else:
		return -1


while stepSize <= 0.09: #cycle through step sizes 
	stepSize += 0.01
	print 'stepSize: ',stepSize
	for i in startingPoints: #cycle through starting points
		iterations = 0
		pos = i
		value = function(i)
		betterSpot = True
		moves = [-stepSize, stepSize]

		while betterSpot:

			betterSpot = False

			newMoves = []

			for j in moves:
				curMove = pos + j
				#print curMove
				if curMove >= 0 and curMove <= 10:
					newMoves.append([function(curMove),curMove])
					#print value
					#print curValue
					
			newMoves.sort(reverse=True)

			if newMoves[0][0] > value:
						value = newMoves[0][0]
						pos = newMoves[0][1]
						betterSpot = True
			#need to swtich back to array and sort!

			#print 'iteration: ',  iterations,  'we are at, ', pos  


			iterations += 1

		#print i,',',pos,',',value,iterations
		print iterations