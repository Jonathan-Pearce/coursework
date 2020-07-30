from collections import deque
from copy import deepcopy
import sys

#BFS

startGrid = [[1,4,2],[5,3,0]]
queue = deque([[startGrid,'']]) #to do BFS
configs = [startGrid] #to avoid revisiting boards
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

while len(queue) > 0 and count < 10:
	tempList = []
	element = queue.popleft()
	#print element
	grid = element[0]
	#print grid
	path = element[1]

	if grid == correctGrid:
		print 'BFS Solution'
		print path[:-2] 
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


	newList = []
	for i in tempList:
		if i[1] not in configs:
			configs.append(i[1])
			newList.append(i)


	#sort list by what element was moved add to queue in that order
	newList.sort()

	for i in newList:
		queue.append([i[1],str(path)+str(i[0])+'->'])

	count += 1


print 'did not find answer :('
