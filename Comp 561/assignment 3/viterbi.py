from sys import stdin, stdout
import sys
import random

letters = ['A', 'V', 'I', 'L', 'M', 'F', 'Y', 'W', 'R', 'H', 'K', 'D', 'E', 'S', 'T', 'N', 'Q', 'C', 'G', 'P']
init = [1/3.0,1/3.0,1/3.0]
#hydrophobic, hydrophilic, mixed
trans = [[4/5.0, 1/25.0, 4/25.0],[3/80.0,7/8.0,7/80.0 ],[1/14.0, 1/14.0,6/7.0]]
ems = [[0.6/8,0.6/8,0.6/8,0.6/8,0.6/8,0.6/8,0.6/8,0.6/8,0.4/12,0.4/12,0.4/12,0.4/12,0.4/12,0.4/12,0.4/12,0.4/12,0.4/12,0.4/12,0.4/12,0.4/12], [0.2/8,0.2/8,0.2/8,0.2/8,0.2/8,0.2/8,0.2/8,0.2/8,0.8/12,0.8/12,0.8/12,0.8/12,0.8/12,0.8/12,0.8/12,0.8/12,0.8/12,0.8/12,0.8/12,0.8/12], [1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0,1/20.0]]

########Variables for questions
hbArray = []
mixedArray = []
lengths = [[],[],[]]
freq = [[],[],[]]
for i in range(3):
    for j in range(len(letters)):
        freq[i].append(0)
stateCount = [0,0,0]       
###############################

####file input
#with open(sys.argv[1], 'r') as f:
#    lines = f.read().splitlines()
#    lines
seq = ""
start = True
with open(sys.argv[1], 'r') as f:
    lines = f.read().splitlines()
    for line in lines:
        if '>' in line:
            table = []
            traceback = []
            currentStates = []
            if start:
                start = False
            else:
                #start of HMM process
                for i in range(3):
                    currentStates.append(init[i] * ems[i][letters.index(seq[:1])])
                table.append(currentStates)
                traceback.append([-1,-1,-1])

                #n-1 columns
                for i in range(1,len(seq)):
                    currentStates = []
                    prev = []
                    for j in range(3):
                        maxScore = -1
                        index = -1
                        for k in range(3):
                            #calculate 3 scores
                            score = table[len(table)-1][k] * trans[k][j] * ems[j][letters.index(seq[i:i+1])]
                            if score > maxScore:
                                maxScore = score
                                index = k
                        prev.append(index)
                        currentStates.append(maxScore)
                    while min(currentStates) < 1:
                        currentStates = [x * 10 for x in currentStates]    
                    table.append(currentStates)
                    traceback.append(prev)
                 

                # HMM traceback
                state = table[len(table)-1].index(max(table[len(table)-1]))
                #print state   
                path = ""
                i = 1
                while state != -1:
                    path = str(state) + path
                    state = traceback[len(traceback)-i][state]
                    i+=1

                #print path
                #print len(path)

                ########### Question A
                hb = 0
                maxhb = 0
                for i in range(len(path)):
                    if path[i:i+1] == '0':
                        hb+=1
                        #print 'here'
                        #print hb
                    else:
                        if hb > maxhb:
                            maxhb = hb
                        #print maxhb
                        hb = 0  
                    if i == len(path)-1 and hb != 0:
                        maxhb = hb 
                hbArray.append(maxhb)             
                ###########################

                ########### Question B
                total = 0
                mixed = 0
                for i in range(len(path)):
                    if path[i:i+1] == '2':
                        mixed+=1
                    total+=1    
                frac = mixed*1.0/total 
                #print frac  
                mixedArray.append(frac)
                ###########################

                ########### Question C
                currentState = ''
                pastState = path[0:1]
                length = 1

                for i in range(1,len(path)):
                    currentState = path[i:i+1]

                    if currentState == pastState:
                        length += 1

                    else:
                        lengths[int(pastState)].append(length)
                        length = 1
                        #print currentState

                    pastState = currentState    

                lengths[int(pastState)].append(length)
                #print lengths
                ################################

                ########### Question D
                for i in range(len(path)):
                    freq[int(path[i:i+1])][letters.index(seq[i:i+1])] += 1
                    stateCount[int(path[i:i+1])] += 1

                #print stateCount
                #print freq 
                #print sum(freq[2])  
                seq = "" 
        else:
            seq += line

#output for questions

print 'Question A'
#A
print hbArray.index(max(hbArray))
print max(hbArray)

print 'Question B'
#B
count = 0
for i in range(len(mixedArray)):
    if mixedArray[i] == 1.0:
        count += 1
print count        

print 'Question C'
#C
for i in range(3):
    print lengths[i]
 
#for i in range(3):
#    lengths[i].sort()
#    lengths[i] = lengths[i][:len(lengths[i])-int(len(lengths[i])*.10)]
#    print lengths[i]


print 'Question D'
#D
for i in range(3):
    for j in range(20):
        freq[i][j] = ((int)(freq[i][j]*1000.0/stateCount[i]))/1000.0
print freq

