import abc


class Classifier:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def classify(self, feature_set):
        return