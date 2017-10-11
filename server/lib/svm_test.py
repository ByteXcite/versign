from classifiers import OneClassSVM
from sklearn.metrics import accuracy_score

import numpy as np
import os, sys
import scipy.io

dir = "features/mydata"
print "Dataset:", dir
print "No. of users:", 1

# Load training data
x_train = []
for f in os.listdir(dir+"/Reference/"):
    if f.endswith(".mat"):
        mat = scipy.io.loadmat(dir+"/Reference/" + f)
        feat = np.array(mat['feature_vector'][0][:])
        x_train.append(feat)

# Load test data
x_test = []
for f in os.listdir(dir+"/Questioned/"):
    if f.endswith(".mat"):
        mat = scipy.io.loadmat(dir+"/Questioned/" + f)
        feat = np.array(mat['feature_vector'][0][:])
        x_test.append(feat)

y_true = np.concatenate([np.ones((30)) * -1, np.ones((5))])

# Get predictions from OneClassSVM
Y_test, Y_train, n_error_train = OneClassSVM(x_train, x_test)
    
# Calculate prediction error
print "Prediction accuracy:", round(accuracy_score(y_true, Y_test)*100, 2), "\n"

os.system("python svm.py features/gpds_signet/development/")
os.system("python svm.py features/gpds_signet/exploitation/")
os.system("python svm.py features/gpds_signet/validation/")
os.system("python svm.py features/mcyt_signet/")
os.system("python svm.py features/cedar_signet/")
