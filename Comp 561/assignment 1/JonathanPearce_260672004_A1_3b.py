import sys

def matchScore(x,y):
   if x == y:
       return match
   elif x == 'A' and y == 'G' or x == 'G' and y == 'A':
       return transition
   elif x == 'C' and y == 'T' or x == 'T' and y == 'C':
       return transition	
   else:
       return transversion

#Input file and variables      
f = open(sys.argv[1], 'r')
line =  ' '
while ('>' not in line):
    line =  f.readline()
s = f.readline() 
s = s[:-1]
s = ' ' + s
line =  ' '
while ('>' not in line):
    line =  f.readline()
t = f.readline() 
t = ' ' + t

#scoring variables
a = int(sys.argv[2])
b = int(sys.argv[3])
match = int(sys.argv[4])
transition = int(sys.argv[5])
transversion = int(sys.argv[6])

#5 dynammic arrays
m = [[0 for i in range(len(t))] for j in range(len(s))]
Ix = [[0 for i in range(len(t))] for j in range(len(s))]
Iy= [[0 for i in range(len(t))] for j in range(len(s))]
Ix3 = [[0 for i in range(len(t))] for j in range(len(s))]
Iy3 = [[0 for i in range(len(t))] for j in range(len(s))]

#5 scoring lists
mScores = [0,0,0,0,0]
IxScores = [0,0,0,0,0]
IyScores = [0,0,0,0,0]
Ix3Scores = [0,0,0,0,0]
Iy3Scores = [0,0,0,0,0]

#First Row
for i in range(len(t)):
    if(i < 3):
        k = i*b
    else:
        k = (i%3)*b + (i - i%3)*a
    m[0][i] = k
    Ix[0][i] = k
    Iy[0][i] = k
    Ix3[0][i] = k
    Iy3[0][i] = k         
#First Column    
for i in range(len(s)):
    if(i < 3):
        k = i*b
    else:
        k = (i%3)*b + (i - i%3)*a
    m[i][0] = k
    Ix[i][0] = k
    Iy[i][0] = k
    Ix3[i][0] = k
    Iy3[i][0] = k


#fill scoring matrices
for i in range(1,len(s)):
    for j in range(1,len(t)):
        mScores[0] = m[i-1][j-1] + matchScore(s[i],t[j])
        mScores[1] = Ix[i-1][j-1] + matchScore(s[i],t[j])
        mScores[2] = Iy[i-1][j-1] + matchScore(s[i],t[j])
        mScores[3] = Ix3[i-1][j-1] + matchScore(s[i],t[j])
        mScores[4] = Iy3[i-1][j-1] + matchScore(s[i],t[j])
        m[i][j] = max(mScores)
        
        IxScores[0] = m[i][j-1] + b
        IxScores[1] = Ix[i][j-1] + b
        IxScores[2] = Iy[i][j-1] + b
        IxScores[3] = Ix3[i][j-1] + b
        IxScores[4] = Iy3[i][j-1] + b
        Ix[i][j] = max(IxScores)
        
        IyScores[0] = m[i-1][j] + b
        IyScores[1] = Ix[i-1][j] + b
        IyScores[2] = Iy[i-1][j] + b
        IyScores[3] = Ix3[i-1][j] + b
        IyScores[4] = Iy3[i-1][j] + b
        Iy[i][j] = max(IyScores)
        
        if j >= 3:
            Ix3Scores[0] = m[i][j-3] + 3*a
            Ix3Scores[1] = Ix[i][j-3] + 3*a
            Ix3Scores[2] = Iy[i][j-3] + 3*a
            Ix3Scores[3] = Ix3[i][j-3] + 3*a
            Ix3Scores[4] = Iy3[i][j-3] + 3*a
            Ix3[i][j] = max(Ix3Scores)
        else:
            Ix3[i][j] = m[i][j]
            
        if i >= 3:
            Iy3Scores[0] = m[i-3][j] + 3*a
            Iy3Scores[1] = Ix[i-3][j] + 3*a
            Iy3Scores[2] = Iy[i-3][j] + 3*a
            Iy3Scores[3] = Ix3[i-3][j] + 3*a
            Iy3Scores[4] = Iy3[i-3][j] + 3*a
            Iy3[i][j] = max(Iy3Scores)
        else:
            Iy3[i][j] = m[i][j]



#Traceback Procedure
i = len(m)-1
j = len(m[0])-1

sAlign = ""
tAlign = ""

print 'Alignment Score:' , max(m[i][j], Ix[i][j], Iy[i][j], Ix3[i][j], Iy3[i][j])
print ' '

while i > 0 or j > 0:
    bScore = max(m[i][j], Ix[i][j], Iy[i][j], Ix3[i][j], Iy3[i][j])
    
    if m[i][j] == bScore:
        sAlign = s[i] + sAlign
        tAlign = t[j] + tAlign
        i -= 1
        j -= 1
    elif Ix[i][j] == bScore:
        sAlign = "-" + sAlign
        tAlign = t[j] + tAlign
        j -= 1
    elif Iy[i][j] == bScore:
        sAlign = s[i] + sAlign
        tAlign = "-" + tAlign
        i -= 1    
    elif j >= 3 and Ix3[i][j] == bScore:
        sAlign = "---" + sAlign
        tAlign = t[j-2] + t[j-1] + t[j] + tAlign
        j -= 3
    elif i >= 3 and Iy3[i][j] == bScore:
        sAlign = s[i-2] + s[i-1] + s[i] + sAlign
        tAlign = "---" + tAlign
        i -= 3
    else:
        print 'should not be here'
        i = 0
        j = 0
        
print 'Final Alignment'
print sAlign
print ' '
print tAlign
