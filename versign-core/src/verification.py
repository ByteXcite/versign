from segment import extract_signature
from src.classifiers import OneClassSVM
from src.libs.sigver_wiwd.process_folder import extract_features

import cv2
import numpy as np
import os
import scipy.io


def verify_cheque(userId, cheque, dirCore=""):
    return verify_signature(userId, extract_signature(cheque, dirCore + "db/models/tree.pkl"), dirCore)

def verify_signature(userId, signature, dirCore=""):
    dirTemp = dirCore + "db/users/" + userId + "/temp/"
    if not os.path.exists(dirTemp):
        os.makedirs(dirTemp)

    cv2.imwrite(dirTemp + "Q001.png", signature)

    # Extract features from questioned signature
    extract_features(dirTemp, dirTemp, dirCore + "src/libs/sigver_wiwd/models/signet.pkl")

    dirTrain = dirCore + "db/users/" + userId + "/features/"
    dirTest = dirTemp

    # Load training data
    x_train = []
    for f in os.listdir(dirTrain):
        if f.endswith(".mat"):
            mat = scipy.io.loadmat(dirTrain + f)
            feat = np.array(mat['feature_vector'][0][:])
            x_train.append(feat)

    # Load test data
    x_test = []
    for f in os.listdir(dirTest):
        if f.endswith(".mat"):
            mat = scipy.io.loadmat(dirTest + f)
            feat = np.array(mat['feature_vector'][0][:])
            x_test.append(feat)

    # Get predictions from OneClassSVM
    Y_test, Y_train, n_error_train, Y_prob = OneClassSVM(x_train, x_test)
    return int(Y_test[0]) == 1