from copy import deepcopy
import sys

#DFS

startGrid = [[[1,4,2],[5,3,0]],0,'']
correctGrid = [[0,1,2],[5,4,3]]

def swapLeft(y,x,currentGrid):
	newGrid = deepcopy(currentGrid)
	newGrid[y][x] = newGrid[y][x-1]
	newGrid[y][x-1] = 0
	#print 'new grid', newGrid
	return [newGrid[y][x], newGrid]

def swapRight(y,x,currentGrid):
	newGrid = deepcopy(currentGrid)
	newGrid[y][x] = newGrid[y][x+1]
	newGrid[y][x+1] = 0
	return [newGrid[y][x], newGrid]

def swapUp(y,x,currentGrid):
	newGrid = deepcopy(currentGrid)
	newGrid[y][x] = newGrid[y-1][x]
	newGrid[y-1][x] = 0
	#print 'new grid', newGrid
	return [newGrid[y][x], newGrid]

def swapDown(y,x,currentGrid):
	newGrid = deepcopy(currentGrid)
	newGrid[y][x] = newGrid[y+1][x]
	newGrid[y+1][x] = 0
	return [newGrid[y][x], newGrid]

count = 0
maxDepth = 0
noSolution = True
while noSolution: #keep increasing depth until we find solution
	maxDepth += 1
	#print maxDepth
	stack = [startGrid] #to do DFS
	configs = [startGrid[0]] #to avoid revisiting boards
	while len(stack) > 0: #keep going while we have new boards to visit
		tempList = []
		element = stack.pop()
		grid = element[0]
		depth = element[1]
		path = element[2]

		#print 'current grid: ' ,grid, ' depth: ',depth

		if grid == correctGrid:
			print 'IDS Solution'
			#print count
			print path[:-2]
			noSolution = False
			sys.exit(0)

		#order of operators: Right, Left, Down, Up
		#top left
		if grid[0][0] == 0:
			tempList.append(swapRight(0,0,grid))
			tempList.append(swapDown(0,0,grid))

		#top middle
		elif grid[0][1] == 0:
			tempList.append(swapRight(0,1,grid))
			tempList.append(swapLeft(0,1,grid))
			tempList.append(swapDown(0,1,grid))

		#top right
		elif grid[0][2] == 0:
			tempList.append(swapLeft(0,2,grid))
			tempList.append(swapDown(0,2,grid))

		#bottom left
		elif grid[1][0] == 0:
			tempList.append(swapRight(1,0,grid))
			tempList.append(swapUp(1,0,grid))

		#bottom middle
		elif grid[1][1] == 0:
			tempList.append(swapRight(1,1,grid))
			tempList.append(swapLeft(1,1,grid))
			tempList.append(swapUp(1,1,grid))

		#bottom right
		else:
			tempList.append(swapLeft(1,2,grid))
			tempList.append(swapUp(1,2,grid))

		#prune list
		newList = []
		for i in tempList:
			if depth + 1 <= maxDepth and i[1] not in configs: #valid depth and unvisited, then lets go!
				configs.append(i[1])
				newList.append(i)

		#sort list by what element was moved add to queue in that order
		newList.sort(reverse=True)
		
		for i in newList:
			stack.append([i[1],depth+1,str(path)+str(i[0])+'->'])

		count += 1


print 'did not find answer :('

