from __future__ import print_function

from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
import numpy as np

# Load training data
x_train = np.load("../../features/4NSigComp2010/TrainingSet/features")
y_train = np.load("../../features/4NSigComp2010/TrainingSet/labels")

# Fit Guassian Naive-Bayes classifier on training data
gnb = GaussianNB()
gnb = gnb.fit(x_train, y_train)

# Fit Bernoulli Naive-Bayes classifier on training data
bnb = BernoulliNB()
bnb = bnb.fit(x_train, y_train)

# Fit Multinomial Naive-Bayes classifier on training data
# mnb = MultinomialNB()
# mnb = mnb.fit(x_train, y_train)

# Load test data
x_pred = np.load("../../features/4NSigComp2010/TestSet/Questioned/features")

# Predict results
G = [6, 15, 28, 29, 34, 49, 52, 66, 87, 90]

# ... using GaussianNB
y_pred = gnb.predict(x_pred)
print("Guassian Naive-Bayes: ", end="")
for i in range(len(y_pred)):
    if y_pred[i] != 0:
        print(i + 1, end=" ")

# ... using BernoulliNB
y_pred = bnb.predict(x_pred)
print("\nBernoulli Naive-Bayes: ", end="")
for i in range(len(y_pred)):
    if y_pred[i] != 0:
        print(i + 1, end=" ")

# ... using MultinomialNB
# y_pred = mnb.predict(x_pred)
# print("\nMultinomial Naive-Bayes: ", end="")
# for i in range(len(y_pred)):
#    if y_pred[i] == 1:
#        print(i + 1, end=" ")
print()