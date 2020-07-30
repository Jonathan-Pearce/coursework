# COMP551 Project 2
Jonathan Pearce, Saima Tazreen, Cristian Groza

# Dependencies
- numpy
- scikitlearn
- scipy
- NLTK

The code consists of two scripts that are controlled with boolean variables
placed at the top of the script. Set the appropriate flag to reproduce the given model/feature set.

# dataProcess.py : run to pre-process features.
  + _sample_ flag to restrict the preprocessing to a 1000 training examples.
  + _removeStopWords_ flag to toggle stop word removal.

# experiments.py : run to produce report results
  + _csv_ flag to toggle Kaggle submission generation. Written in _submission.csv_.
  + _tfidf\_pipeline_ flag to run models on TFIDF features.
  + _vad_ flag to add valence, arousal, dominance features.
  + _connot_ flag to add positive/negative opinion and connotation counts.
  + _crossvalidate_ flag to print cross-validation results for the model.
  + _model_ variable to the chosen model for submission generation.

# Replicating Kaggle accuracy
## In experiments.py
1. Set the _model_variable to linear_model.LogisticRegression(C=10, penalty = 'l2').
2. Set the _vad_, _connot_ flags to False.
3. Set _crossvalidate_ to False.
4. Set _csv_ to True.

## In dataProcess.py
1. Set _sample_ to False.
2. Set _removeStopWords_ to True.
## Submission generation
1. Run _dataProcess.py_
2. Run _experiments.py_

Resulting csv file is written in submission.csv.

# Replicating report results

To replicate the report results, we must set the appropriate flags corresponding to the specific result. For example, if we want to replicate the result of binary features, we must:
1. Set _crossvalidate_ to True.
2. Set_tfidf\_pipeline_ to False.
3. Run _experiments.py_

The script will run cross-validation on all three models and print the results together with the average accuracy.

# Naive Bayes

Run the file naiveBayes.py to replicate this specific result separately.



