from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm, preprocessing

# Load training data
X_train = preprocessing.robust_scale(np.load("../../features/4NSigComp2010/TrainingSet/features"))
Y_train = np.load("../../features/4NSigComp2010/TrainingSet/labels")

x_train = []
y_train = []
for i in range(len(Y_train)):
    if Y_train[i] == 2:
        x_train.append(X_train[i])
        y_train.append(Y_train[i])

# Fit One-Class SVM on training data
clf = svm.OneClassSVM(nu=0.5, kernel="rbf", gamma=2**-11)
clf.fit(x_train)

# Load test data
x_test = preprocessing.robust_scale(np.load("../../features/4NSigComp2010/TestSet/Questioned/features"))

# Predict results
G = [6, 15, 28, 29, 34, 49, 52, 66, 87, 90]
y_pred_train = clf.predict(x_train)
y_pred_test = clf.predict(x_test)

# Calculate prediction error
n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size

# plot the line, the points, and the nearest vectors to the plane
print(n_error_train)
print(n_error_test)

g = []
for i in range(len(y_pred_test)):
    if y_pred_test[i] == 1:
        g.append(i + 1)

print(G)
print(g)