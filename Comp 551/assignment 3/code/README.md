Packages Used: Numpy, Pandas, os, cv2, matplotlib.pyplot, pickle, tensorflow, keras, sklearn
Also used: Google Colab notebook for neural network training/testing

***Replication Procedure***

1)Data Processing (Filename: imageProcessing.py)
Ensure data files are inside folder named input
Run imageProcessing.py (will produce a file named 'trainCrop.pkl')
Change 'train' boolean value to 'False' (Line 14)
Run imageProcessing.py (will produce a file named 'testCrop.pkl')

2)Scikit Learn Models (Random Forest and K-nearest neighbors) (Filename: slearn_experiments.ipynb)
Ensure 'trainCrop.pkl' and 'testCrop.pkl' are loaded into environment
Run all code blocks in order (produces a submission formatted file named 'predictions.csv')


3)Neural Network Models (Filename: 551.ipynb)
3.1) 2 Layer Fully connected model
Ensure 'trainCrop.pkl' is loaded into environment
Change 'epochs' to 16 in Block 7 line 3
Run Code Block 1-2,4-5 and 7

3.2) LeNet-5 CNN
Ensure 'trainCrop.pkl' and 'testCrop.pkl' are loaded into environment
Change 'epochs' to 13 in Block 7 line 3
Run Code Blocks 1-4 and 6-10 (will produce a submission file named 'results.csv')