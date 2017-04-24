import Classifier
from math import exp
from numpy import transpose, array, ndarray


class LogisticClassifier:
    def g(self, Z):
        G = []
        for z in Z:
            G.append(1 / (1 + exp(-z)))
        return G

    def h(self, theta, x):
        return self.g(transpose(theta).dot(x))

    def cost(self, h, y):
        pass

    def classify(self, allFeatures):
        ndarray(shape=(7, 1))
        theta = array([1, 1, 1, 1, 1, 1, 1])

        X = []
        for featureSet in allFeatures:
            f = list(featureSet[sorted(featureSet.keys())[0]])
            f[2] = f[2][0] + f[2][1]
            X.append(f)

        ndarray(shape=(2, 7))
        X = array(X).transpose()

        print "theta = ", theta
        print "X = ", X
        return self.h(theta, X)