from __future__ import print_function

import numpy as np


class NeuralNetwork:
    def __nonlin(self, x, derivative=False):
        if derivative:
            return x * (1 - x)

        try:
            return 1 / (1 + np.exp(-x))
        except RuntimeWarning:
            return 0

    def feed_forward(self, l0, syn0):
        return self.__nonlin(np.dot(l0, syn0))

    def train(self, X, Y, iterations):
        # initialize weights randomly with mean 0
        syn0 = 2 * np.random.random((len(X[0]), 1)) - 1

        for iter in range(iterations):
            # forward propagation
            l0 = X
            l1 = self.feed_forward(l0, syn0)

            # how much did we miss?
            l1_error = Y - l1

            if iter % 10000 == 0:
                print("i:", iter, "Loss:", np.mean(l1_error))

            # multiply how much we missed by the
            # slope of the sigmoid at the values in l1
            l1_delta = l1_error * self.__nonlin(l1, derivative=True)

            # update weights
            update = np.dot(l0.T, l1_delta)
            syn0 += update

        return [syn0]  # , syn1, syn2, syn3
