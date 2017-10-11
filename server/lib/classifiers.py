from sklearn import svm, preprocessing
import scipy.io
import os

def OneClassSVM(x_train, x_test):
    # Scale input arrays
    #x_train = preprocessing.scale(x_train)
    #x_test = preprocessing.scale(x_test)

    # Fit SVM model
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=2**-11)
    clf.fit(x_train)

    # Calculate model error
    Y_train = clf.predict(x_train)
    n_error_train = Y_train[Y_train == -1].size

    # Predict results
    Y_test = clf.predict(x_test)

    return Y_test, Y_train, n_error_train