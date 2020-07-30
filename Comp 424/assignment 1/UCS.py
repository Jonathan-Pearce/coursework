import Queue as Q
from copy import deepcopy
import heapq
import sys

#UCS

startGrid = (0,[[1,4,2],[5,3,0]],'')
pqueue = Q.PriorityQueue(startGrid) #uniform search
configs = [startGrid[1]] #to avoid revisiting boards
correctGrid = [[0,1,2],[5,4,3]]

pqueue.put(startGrid)


def swapLeft(y,x,currentGrid,curCost):
	newGrid = deepcopy(currentGrid)
	newGrid[y][x] = newGrid[y][x-1]
	newGrid[y][x-1] = 0
	#print 'new grid', newGrid
	return [curCost+1,newGrid[y][x], newGrid]

def swapRight(y,x,currentGrid,curCost):
	newGrid = deepcopy(currentGrid)
	newGrid[y][x] = newGrid[y][x+1]
	newGrid[y][x+1] = 0
	return [curCost+1,newGrid[y][x], newGrid]

def swapUp(y,x,currentGrid,curCost):
	newGrid = deepcopy(currentGrid)
	newGrid[y][x] = newGrid[y-1][x]
	newGrid[y-1][x] = 0
	#print 'new grid', newGrid
	return [curCost+1,newGrid[y][x], newGrid]

def swapDown(y,x,currentGrid,curCost):
	newGrid = deepcopy(currentGrid)
	newGrid[y][x] = newGrid[y+1][x]
	newGrid[y+1][x] = 0
	return [curCost+1,newGrid[y][x], newGrid]

count = 0

while not pqueue.empty() and count < 10:
	tempList = []
	element = pqueue.get()
	cost = element[0]
	grid = element[1] 
	path = element[2]
	#print grid,' ',cost

	if grid == correctGrid:
		print 'UCS Solution'
		print path[:-2]
		sys.exit(0)

	#order of operators: Right, Left, Down, Up
	#top left
	if grid[0][0] == 0:
		tempList.append(swapRight(0,0,grid,cost))
		tempList.append(swapDown(0,0,grid,cost))

	#top middle
	elif grid[0][1] == 0:
		tempList.append(swapRight(0,1,grid,cost))
		tempList.append(swapLeft(0,1,grid,cost))
		tempList.append(swapDown(0,1,grid,cost))

	#top right
	elif grid[0][2] == 0:
		tempList.append(swapLeft(0,2,grid,cost))
		tempList.append(swapDown(0,2,grid,cost))

	#bottom left
	elif grid[1][0] == 0:
		tempList.append(swapRight(1,0,grid,cost))
		tempList.append(swapUp(1,0,grid,cost))

	#bottom middle
	elif grid[1][1] == 0:
		tempList.append(swapRight(1,1,grid,cost))
		tempList.append(swapLeft(1,1,grid,cost))
		tempList.append(swapUp(1,1,grid,cost))

	#bottom right
	else:
		tempList.append(swapLeft(1,2,grid,cost))
		tempList.append(swapUp(1,2,grid,cost))


	newList = []
	for i in tempList:
		if i[2] not in configs:
			configs.append(i[2])
			newList.append(i)


	#sort list by what element was moved add to queue in that order
	newList.sort(key=lambda x: x[1])

	for i in newList:
		pqueue.put((i[0],i[2],str(path)+str(i[1])+'->'))

	count += 1


print 'did not find answer :('

