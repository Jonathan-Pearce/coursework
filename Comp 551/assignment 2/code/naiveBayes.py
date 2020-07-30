import numpy as np
from collections import Counter
from math import log
import io
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import KFold
from scipy import sparse
import time

# X is input binary data
# Y is class data
def train(X,y):
	#count number of instance with y=0 and y=1
    label_counts = Counter(y)
    N = label_counts[1] + label_counts[0]
    N_1 = float(label_counts[1])
    N_0 = float(label_counts[0])

    #probability of data point being y=1
    p_1 = N_1/N

    #log(theta_1 / (1-theta_1))
    #class probability calculation
    p = log(p_1/(1-p_1))

    #partition data by response variable
    zeroes = []
    ones = []

    for i in range(len(y)):
        if y[i] == 1:
            ones.append(i)
        else:
            zeroes.append(i)

    #Size of X
    rows, cols  = np.shape(X)
    features = []

    #X_0 contains all data instances with response y=0
    X_0 = np.delete(X, ones, axis=0)

    #build sparse matrix
    #complete columns sums
    data_csr = sparse.csr_matrix(X_0)
    sums = data_csr.sum(axis=0)
    sums_0 = sums.tolist()

    #save memory
    del X_0
    
    #X_1 contains all data instance with response y=1
    X_1 = np.delete(X, zeroes, axis=0)

    #save memory
    del X
    
    #build sparse matrix
    #complete columns sums
    data_csr = sparse.csr_matrix(X_1)
    sums = data_csr.sum(axis=0)
    sums_1 = sums.tolist()

    #save memory
    del X_1

    #go through each column
    for i in range(cols):
        
        #counts for instance with x_i = 1 | y=0 
        #with laplace smoothing
        p_10 = (sums_0[0][i]+1)/(N_0+2)

        #counts for instance with x_i = 1 | y=1
        #with laplace smoothing
        p_11 = (sums_1[0][i]+1)/(N_1+2)
        
        #take logarithms of the ratios
        f_1 = log(p_11/p_10)
        f_0 = log((1-p_11)/(1-p_10))

        #add values to feature set
        features.append([f_0,f_1])

    #return feature and class probability
    return features,p

def predict(X,features,p):
	#data point score
    sigma = 0

    #shape of test set
    rows, cols  = np.shape(X)

    #reponse vector
    response = []

    #iterate through test set
    for i in range(rows):
        for j in range(cols):
        	#add feature score to data point score
            sigma += features[j][X[i,j]]
        #add class probability
        sigma += p

        #Decision boundary of sigma = 0 
        if sigma > 0:
            response.append(1)
        else:
            response.append(0)
        #reset value
        sigma = 0

    return response

def accuracy(labels, predict):
    total = float(len(labels))
    correct = 0

    #calculate number of correct responses
    for i in range(len(labels)):
        if labels[i] == predict[i]:
            correct += 1

    #return fold accuracy
    return correct/total


#to ensure the same splits in cross validation 
random_seed = 7

#for timing code
t0_full = time.time()

##Data Input

#positive text
pos = []
#negative text
neg = []
#Read data
positive = io.open('data_stopwords.pos', encoding = "ISO-8859-1")
negative = io.open('data_stopwords.neg', encoding = "ISO-8859-1")

#add data to correct list
for line in positive:
    line = line.strip() 
    pos.append(line)

for line in negative:
    line = line.strip()
    neg.append(line)

#Use half the dataset
#Using full dataset is very slow on Trottier computers
pos = pos[0:6250]
neg = neg[0:6250]

#Build full set of data and responses
X = pos + neg
y = [1]*len(pos) + [0]*len(neg)

#Build KFold 
kf = KFold(n_splits=5,shuffle=True,random_state = random_seed)
#fold accuracies
acc_scores = []
#fold counter
j = 1

#iterate through folds
for train_index, test_index in kf.split(X):

	#Build train and test sets based on current fold
    X_train = [X[i] for i in train_index] 
    X_test = [X[i] for i in test_index]

    y_train = [y[i] for i in train_index]
    y_test = [y[i] for i in test_index]
    
    #build count vectorizer on train data only
    #binary, ngrams, all words
    count_vect = CountVectorizer(binary = True,ngram_range=(1, 1)).fit(X_train);
    #transform train and test set according to count vectorizer
    X_train_binary = count_vect.transform(X_train)
    X_test_binary = count_vect.transform(X_test) 

    #train custom naive bayes model
    features,p = train(X_train_binary.toarray(), y_train)

    #predict test set using custom predict function
    y_predict = predict(X_test_binary.toarray(),features,p)

    #calculate and store fold accuracy
    acc_scores.append(accuracy(y_test,y_predict))
    print 'Done fold: ', j
    j += 1

#print fold accuracies
print acc_scores
#print fold average
print sum(acc_scores)/5

#print run time
t1 = time.time()
print 'full time',t1-t0_full