from sys import stdin, stdout
import sys
import random
import math
import itertools
from datetime import datetime

print str(datetime.now())

#chnage this variable to adjust length of sequence
c_length = 6
#stores all permutations of length c_length
seqCombo = [0] * int(math.pow(4,c_length))
bpScore = {'A':0, 'C':1, 'G':2, 'T':3}
lengths = [] #holds all the lengths of the sequences, will be used for E(C)
count = {'A':0, 'C':0, 'G':0, 'T':0} #counts each base pair
prob = [0,0,0,0]#prob of each base pair

#find index of seq in seqCombo
def getindex(seq):
	score = 0
	for i in range(len(seq)):
		char = seq[i:i+1]
		score += int(bpScore[char]*math.pow(4,i))
	return score

#convert tuple into string
def toString(bpList):
    string = ''
    for i in bpList:
    	string += i
    return string	

#input
seq = ""
start = True
counter = 0
with open(sys.argv[1], 'r') as f:
    lines = f.read().splitlines()
    for line in lines:
        if counter % 1000 == 0:
            print counter
        counter += 1
        if '>' in line:
            n = 0
            if start:
                start = False
            else:
                #length of sequence
                lengths.append(len(seq))
                #count base pairs
                for i in range(len(seq)):
            	    char = seq[i:i+1]
            	    count[char] += 1
                #check all sequences of length c_length and record them        
                for i in range(len(seq) - c_length):
            	    partialSeq = seq[i:i+c_length]
            	    index = getindex(partialSeq)
            	    #print partialSeq
            	    #print index
            	    seqCombo[index] = seqCombo[index] + 1
        else:
            seq += line	

#print seqCombo  
#print lengths
#print count 

#calculating probability of each base pair
totalBP = sum(lengths)
prob[0] = count['A']*1.0/totalBP
prob[1] = count['C']*1.0/totalBP
prob[2] = count['G']*1.0/totalBP
prob[3] = count['T']*1.0/totalBP
#print prob

############################################################

#all possible options for consesus sequence
bp = [['A'],['C'],['G'],['T'],['A','G'],['C','T'],['A','C','G','T']]

#generate all combinations 
perm = list(itertools.product(bp, repeat=c_length))

#calculate number of possible start posistions 
#for a sequence of length c_length for E(C) calculation
startPos = 0
for i in range(len(lengths)):
    startPos += lengths[i] - c_length + 1

#zscore and zseq, these will store optimal sequence and its corresponding score!
zScore = -100000
zSeq = None

#go through all permuations
for i in range(len(perm)):
    allSeq = []
    #find all sequences that can be made out consensus sequence
    for element in itertools.product(*perm[i]):
        allSeq.append(toString(element))
    #print allSeq

    nC = 0
    eC = 0
    #calculate N(C)
    #iterate through all possible sequences and add there occurences
    for j in allSeq:
    	index = getindex(j)
    	nC += seqCombo[index]
    #print nC	

    #calculate E(C)
    #iterate through all possible sequences
    totalProb = 0
    for k in allSeq:
    	tempProb = 1
        #iterate through each 
    	for l in range(len(k)):
    		charProb = prob[bpScore[k[l:l+1]]]
    		#print charProb
    		tempProb *= charProb
    	#print tempProb
    	totalProb += tempProb
    #print totalProb
    eC = totalProb * startPos



    #calculate z score
    zC = (nC-eC)/math.sqrt(eC)

    if zC > zScore:
    	zScore = zC
    	zSeq = perm[i]
    	print zScore
    	print perm[i]

print len(perm)

print str(datetime.now())




