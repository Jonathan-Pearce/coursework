"""
The goal of this module is to process raw json file into inputs X and outputs y 

The important function in process_features:
    takes the proj1_data.json file  as argument
    and returns X, y which are numpy arrays 
    X is 2d 12000 x 163,  y is 1d 12000 x 1
"""
import sys
import os
import json
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def read_json_file(f):
    data = []
    with open(os.path.abspath(f)) as fp:
        data = json.load(fp)

    return data

def process_features(data, length, freq, most_frequent_words):
    X = []
    y = []
    i = 0
    for row in data:
        y.append(row["popularity_score"])

        #print length[i]
        newLength = [length[i][0]]

        x_i = [1.0, int(row["children"]), float(row["controversiality"]), int(bool(row["is_root"]))] + [int(row["children"]) * int(row["children"])] + [int(row["children"])*length[i][0]] + process_text(row["text"], most_frequent_words)
        #print x_i
        #print len(x_i)
        #sys.exit(0)
        X.append(x_i)
        i += 1 

    return np.array(X), np.array(y)

def apply_nltk_stuff(all_words):
    stop_words = set(stopwords.words("english"))
    return [w for w in all_words if w.isalpha() and w not in stop_words]

def count_words(text, k, apply_nltk_stuff=False):
    if apply_nltk_stuff:
        stop_words = set(stopwords.words("english"))

    all_words = {}
    for string in text:
        if apply_nltk_stuff:
            raw_words = word_tokenize(string.lower())
            words = [w.lower() for w in raw_words if w.isalpha() and w not in stop_words]
        else:
            words = string.lower().split()
        for word in words:
            if word in all_words:
                all_words[word] += 1
            else:
                all_words[word] = 1

    top_k_words = sorted(all_words.items(), key=lambda t: t[1], reverse=True)[0:k]
    return [tup[0] for tup in top_k_words] 

def process_text(string, most_frequent_words, apply_nltk_stuff=False):
    word_counts = {}
    word_features = []
    if apply_nltk_stuff:
        words = word_tokenize(string.lower())
    else:
        words = string.lower().split()
    
    for word in words:
        if word in word_counts:
            word_counts[word] +=1
        else:
            word_counts[word] = 1

    for word in most_frequent_words:
        if word in word_counts:
            word_features.append(word_counts[word])
        else:
            word_features.append(0)

    #print len(word_features)
    #print word_features
    return word_features

#custom feature
def text_length(text):
    feature = []
    for string in text:
        #print string
        string = string.lower().split(' ')
        #print string

        textLength = [len(string)]

        feature.append(textLength)
        #print len(string)

    return feature

#custom feauture
def stopWordFreq(text):
    feature = []

    stop_words = set(stopwords.words("english"))

    for string in text:
        string = string.lower().split(' ')

        textLength = len(string)

        numStopWords = 0
        for i in string:
            if i in stop_words:
                numStopWords += 1

        score = 1.0 - (numStopWords*1.0)/textLength

        feature.append([score])

    #print feature[0:20]    
    return feature



def train_validate_test_split(X, y):
    train_X, train_y = X[:10000], y[:10000]
    validate_X, validate_y = X[10000:11000], y[10000:11000]
    test_X, test_y = X[11000:12000], y[11000:12000]

    return train_X, train_y, validate_X, validate_y, test_X, test_y

def main(args):
    data = read_json_file(args[0])
    most_frequent_words = count_words([row["text"] for row in data], 160)
    print(most_frequent_words)
    X, y = process_features(data, most_frequent_words)
    train_X, train_y, validate_X, validate_y, test_X, test_y = train_validate_test_split(X, y)
    print("INPUT MATRIX X: \n{}".format(X))
    print("OUTPUT VECTOR Y: \n{}".format(y))

if __name__ == "__main__": main(sys.argv[1:])
