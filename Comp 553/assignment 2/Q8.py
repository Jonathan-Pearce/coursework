grid = [
[26, 8, 59, 5, 42, 17, 6, 34], 
[11, 18, 53, 9, 40, 22, 17, 35],
[19, 25, 50, 24, 49, 23, 21, 31],
[2, 3, 52, 3, 45, 14, 21, 38],
[1, 23, 54, 28, 47, 17, 14, 33], 
[22, 27, 57, 27, 43, 19, 23, 36], 
[21, 19, 55, 28, 46, 16, 5, 32],
[20, 12, 56, 18, 41, 16, 10, 39],
[2, 4, 58, 28, 48, 26, 15, 30],
[20, 9, 51, 10, 44, 20, 6, 37]]

def score(arrange,grid,n):
	#print arrange
	score = 0
	for i in range(n):
		score += grid[arrange[i]][i]
		#print score

	return score


def vcgMechansim(grid):
	#players
	k = len(grid)

	l = []
	for i in range(k):
		l.append(i)	

	#items
	n = len(grid[0])


	maxScore = 0
	maxArrange = []
	

	arrange = [0]
	l[0] = -1
	previousPlayer = 0
	itemFound = True


	while(len(arrange) > 0):

		#print arrange

		if not itemFound:
			#remove the last index from the arrangment
			player = arrange.pop()
			#replace -1 with value
			l[player] = player
			previousPlayer = player

		#we need more people
		if len(arrange) < n:
			itemFound = False
			#we need to add a number
			for i in l:
				#we have found an available person
				if i != -1 and i > previousPlayer and not itemFound:
					arrange.append(i)
					previousPlayer = -1
					l[i] = -1
					itemFound = True

		#if we have a solution
		if len(arrange) == n:
			#evaluate
			arrangeScore = score(arrange,grid,n)
			if arrangeScore >= maxScore:
				maxScore = arrangeScore
				maxArrange = arrange[:]

			#remove the last index from the arrangment
			player = arrange.pop()
			#replace -1 with value
			l[player] = player
			previousPlayer = player

		
	return maxScore,maxArrange



#VCG with everyone
Maxscore,Maxarrange = vcgMechansim(grid)

#print Maxscore
#print [i+1 for i in Maxarrange]

payments = []


#Now redo the auction without each person that claimed an item in the VCG auction
for i in range(8):
	#player i's bid vector
	playerBid = grid[Maxarrange[i]]
	#delete player i's bid vector from bid array
	del grid[Maxarrange[i]]

	scoreMinusI,arrangeMinusI = vcgMechansim(grid)
	#print scoreMinusI

	#calculate payments
	#Best result without player i - old result without i's payment
	payments.append(scoreMinusI - (Maxscore - playerBid[i]))

	#add bid vector back in
	grid.insert(Maxarrange[i],playerBid)



#print payments
#print sum(payments)

print 'Welfare Maximization: ',Maxscore
for i in range(8):
	print 'Player ',Maxarrange[i]+1,' won item ',i+1,' and paid a price of ',payments[i]
print 'Sum of payments: ',sum(payments)


