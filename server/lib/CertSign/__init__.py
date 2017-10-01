# coding: iso-8859-15
"""
Distance Threshold (DT): The DT method is the common signature verification
model. The first step is to enroll genuines K as reference signatures. The
distance d(X, Y) is computed for each pair (X, Y ) in K to determine the
threshold thres = max{d(X, Y )|X, Y â K}. Given a questioned signature Q,
the average of {d(Q, Y)|Y â K}, denoted as dist, is computed. If dist < thres,
then Q is accepted as a genuine; and rejected otherwise.

Srihari, S. N., Xu, A., & Kalera, M. K. (2004, October).
Learning strategies and classification methods for off-line signature verification.
In Frontiers in Handwriting Recognition, 2004. IWFHR-9 2004. Ninth International Workshop on (pp. 161-166). IEEE.
"""

from __future__ import print_function

import itertools

import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
from sklearn import svm, preprocessing

from FeatureExtractor import FeatureExtractor
from ImageProcessor import ImageProcessor
from NeuralNetwork import NeuralNetwork


def find_image_files(dir):
    # type: (str) -> list
    images = []
    if os.path.isdir(dir) or os.path.isdir(dir + "/"):
        if not dir.endswith("/"):
            dir += "/"

        for f in os.listdir(dir):
            images += find_image_files(dir + f)
            if f.endswith(".png") or f.endswith(".jpg"):
                images.append(dir + f)

    return images


def scale_features(features_nxm):
    # type: (list) -> list
    """
    Takes a (n x m) matrix where each of the n rows represents one signature
    with values of m different features extracted from that signature.

    The function scales each of the m features to range (0,1) and returns a
    (n x m) matrix.

    :param features_nxm: n x m matrix of signature features
    :return: n x m matrix of scaled signatrue features
    """
    temp_mxn = [[],  # 0 Aspect ratio
                [],  # 1 Black pixel count
                [],  # 2 Black pixel average inclination
                [],  # 3 CentroidX
                [],  # 4 CentroidY
                [],  # 5 Centroid inclination
                [],  # 6 Kurtosis
                [],  # 7 Normalized size
                [],  # 8 Skewness
                [],  # 9 Standard deviation
                []]  # 10 Transitions

    # Take transpose of the n x m matrix
    for sign in features_nxm:
        for i in range(len(sign)):
            temp_mxn[i].append(sign[i])

    # Add minimum row value to each of the element of a row to shift negative values
    for i in range(len(temp_mxn)):
        for j in range(len(temp_mxn[i])):
            temp_mxn[i][j] += min(temp_mxn[i])

    # Divide each row element with max of that row to get a value in (0, 1)
    for i in range(len(temp_mxn)):
        for j in range(len(temp_mxn[i])):
            temp_mxn[i][j] /= max(temp_mxn[i])

    # Take transpose of the m x n matrix
    features_nxm = []
    for sign in temp_mxn:
        sign = []
        for i in range(len(sign)):
            sign.append(sign[i])

        features_nxm.append(sign)

    return features_nxm


def save_features(training_dir):
    print("Extracting features ...")
    F = []
    L = []
    improc = ImageProcessor()
    ftextr = FeatureExtractor()
    img_files = find_image_files(training_dir)
    count = 1.0
    for ifile in img_files:
        done = count / len(img_files) * 100
        print("\r[", end="")
        for i in range(int(done)):
            print("|", end="")
        for i in range(100 - int(done)):
            print(" ", end="")
        print("] " + ifile + ", " + str(round(done, 2)) + "%", end="")
        count += 1
        signature = Image.open(ifile)
        processed = improc.preprocess(signature)
        F.append(ftextr.extract_features(processed))

        if ifile.startswith("dataset/TrainingSet/D"):
            L.append(1)
        elif ifile.startswith("dataset/TrainingSet/G"):
            L.append(2)
        elif ifile.startswith("dataset/TrainingSet/R"):
            L.append(3)
        else:
            L.append(0)

    np.ndarray(shape=(len(F), len(F[0])))
    F = np.array(F)
    F.dump(training_dir + "feature_dump")

    np.ndarray(shape=(len(L), 1))
    L = np.array(L)
    L.dump(training_dir + "label_dump")


def train_network(feature_dir):
    print("Training neural netrowk ...")
    x_train = np.load(feature_dir + "feature_dump")
    y_train = np.load(feature_dir + "label_dump")[:, None]
    x_train_temp = []
    y_train_temp = []
    for i in range(len(y_train)):
        if y_train[i] == 0:
            x_train_temp.append(x_train[i])
            y_train_temp.append(-1)
        elif y_train[i] == 3:
            x_train_temp.append(x_train[i])
            y_train_temp.append(1)

    x_train = np.asarray(x_train_temp)
    y_train = np.asarray(y_train_temp)[:, None]

    syn = NeuralNetwork().train(x_train, y_train, 50000)

    print("Saving training results ...")
    i = 0
    for s in syn:
        s.dump(feature_dir + "syn" + str(i))
        i += 1


def test_signature(test_dir):
    F = []
    improc = ImageProcessor()
    ftextr = FeatureExtractor()
    img_files = find_image_files(test_dir)
    count = 1.0
    for ifile in img_files:
        print("Extracting features, " + str(round(count / len(img_files) * 100, 1)) + "% done ...")
        count += 1
        signature = Image.open(ifile)
        processed = improc.preprocess(signature)
        F.append(ftextr.extract_features(processed))

    np.ndarray(shape=(len(F), len(F[0])))
    F = np.array(F)

    np.ndarray(shape=(len(F), len(F[0])))
    F = np.array(F)
    F.dump(test_dir + "feature_dump")


def get_accuracy(predictions):
    correct = 0
    genuine = [49, 52, 66, 6, 15, 28, 29, 34, 87, 90]
    for i in range(len(predictions)):
        if i in genuine and predictions[i] == 1: # or i not in genuine and predictions[i] == -1:
            correct += 1

    return float(correct) / len(genuine) * 100


def predict_with_mlp():
    combinations = []
    for i in range(1, 12):
        combs = itertools.combinations(range(11), r=i)
        for c in combs:
            combinations.append(list(c))

    selected = []
    for features in combinations:
        # Load and scale test features
        l0 = np.load("dataset/TestSet/Questioned/feature_dump")[:, features]
        syn0 = np.load("dataset/TrainingSet/syn0")[features, :]

        network = NeuralNetwork()
        predictions = network.feed_forward(l0, syn0)

        mean = np.mean(predictions)
        for i in range(len(predictions)):
            if predictions[i] < mean:
                predictions[i] = -1
            else:
                predictions[i] = 1

        accuracy = get_accuracy(predictions)
        plot(predictions, title=str(features) + ", Accuracy: " + str(accuracy) + "%")
        if selected == [] or selected[0] < accuracy:
            selected = [accuracy, features, predictions]

    print(selected)
    plot(selected[2], title=str(selected[1]) + ", Accuracy: " + str(selected[0]) + "%")


def predict_with_svm():
    # Load and scale training features
    x_train = np.load("dataset/TrainingSet/feature_dump")[:, [5, 10]]
    x_train = preprocessing.scale(x_train)

    # Load corresponding labels
    y_train = np.load("dataset/TrainingSet/label_dump")
    x_train_temp = []
    y_train_temp = []
    for i in range(len(y_train)):
        if y_train[i] == 0:
            x_train_temp.append(x_train[i])
            y_train_temp.append(-1)
        elif y_train[i] == 3 or y_train[i] == 2:
            x_train_temp.append(x_train[i])
            y_train_temp.append(1)

    x_train = x_train_temp
    y_train = y_train_temp

    # Fit one-class SVM model
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=1.0, verbose=True, max_iter=1000)
    clf.fit(X=x_train, y=y_train)

    # Load and scale test features
    x_test = np.load("dataset/TestSet/Questioned/feature_dump")[:, [5, 10]]
    x_test = preprocessing.scale(x_test)

    # Predict and plot results
    predictions = clf.predict(x_test)
    plot(predictions)


def plot(predictions, xlabel="Signature", ylabel="Prediction", title=""):
    GX = [49, 52, 66]
    GY = []

    DX = [6, 15, 28, 29, 34, 87, 90]
    DY = []

    FX = []
    FY = []
    for i in range(len(predictions)):
        if i + 1 in GX:
            GY.append(predictions[i])
        elif i + 1 in DX:
            DY.append(predictions[i])
        else:
            FX.append(i + 1)
            FY.append(predictions[i])

    plt.plot(FX, FY, 'o', c='r')
    plt.plot(GX, GY, 'o', c='g')
    plt.plot(DX, DY, 'o', c='b')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
    plt.close()
