from numpy import mean, log, exp, std, median, power


class KNNClassifier:
    def __distMinkowski(self, X1, X2, p):
        # type: (list, list, float) -> float
        d = 0
        for i in range(len(X1)):
            d += pow(abs(float(X1[i]) - float(X2[i])), p)
        d = power(d, 1.0 / p)
        return d

    def __distEuclidean(self, X1, X2):
        # type: (list, list) -> float
        return self.__distMinkowski(X1, X2, 2)

    def __distManhattan(self, X1, X2):
        # type: (list, list) -> float
        return self.__distMinkowski(X1, X2, 1)

    def __distHamming(self, X1, X2):
        # type: (list, list) -> float
        return self.__distMinkowski(X1, X2, 0.01)

    def __distSigmoid(self, X1, X2):
        # type: (list, list) -> float
        d = 0
        for i in range(len(X1)):
            d += 1 / (1 + exp(-abs(float(X1[i]) - float(X2[i]))))
        return d

    def __distKLDivergence(self, X1, X2):
        # type: (list, list) -> float
        d = 0
        for i in range(len(X1)):
            if float(X2[i]) != 0:
                d += float(X1[i]) * log(float(X1[i]) / float(X2[i]))
        return -d

    def distance(self, referenceFeatureSet, questionedFeatureSet):
        # type: (dict, dict) -> list
        D = []
        dist = {}
        for key in referenceFeatureSet:
            if key in questionedFeatureSet:
                dist[key] = []
                dist[key].append(
                    self.__distEuclidean([referenceFeatureSet[key][0]], [float(questionedFeatureSet[key][0])]))
                dist[key].append(
                    self.__distEuclidean([referenceFeatureSet[key][1]], [float(questionedFeatureSet[key][1])]))
                dist[key].append(self.__distEuclidean(referenceFeatureSet[key][2], questionedFeatureSet[key][2]))
                dist[key].append(
                    self.__distEuclidean([referenceFeatureSet[key][3]], [float(questionedFeatureSet[key][3])]))
                dist[key].append(
                    self.__distEuclidean([referenceFeatureSet[key][4]], [float(questionedFeatureSet[key][4])]))
                dist[key].append(
                    self.__distEuclidean([referenceFeatureSet[key][5]], [float(questionedFeatureSet[key][5])]))
        D.append(dist)

        dist = {}
        for key in referenceFeatureSet:
            if key in questionedFeatureSet:
                dist[key] = []
                dist[key].append(
                    self.__distManhattan([referenceFeatureSet[key][0]], [float(questionedFeatureSet[key][0])]))
                dist[key].append(
                    self.__distManhattan([referenceFeatureSet[key][1]], [float(questionedFeatureSet[key][1])]))
                dist[key].append(self.__distManhattan(referenceFeatureSet[key][2], questionedFeatureSet[key][2]))
                dist[key].append(
                    self.__distManhattan([referenceFeatureSet[key][3]], [float(questionedFeatureSet[key][3])]))
                dist[key].append(
                    self.__distManhattan([referenceFeatureSet[key][4]], [float(questionedFeatureSet[key][4])]))
                dist[key].append(
                    self.__distManhattan([referenceFeatureSet[key][5]], [float(questionedFeatureSet[key][5])]))
        D.append(dist)

        dist = {}
        for key in referenceFeatureSet:
            if key in questionedFeatureSet:
                dist[key] = []
                dist[key].append(
                    self.__distHamming([referenceFeatureSet[key][0]], [float(questionedFeatureSet[key][0])]))
                dist[key].append(
                    self.__distHamming([referenceFeatureSet[key][1]], [float(questionedFeatureSet[key][1])]))
                dist[key].append(self.__distHamming(referenceFeatureSet[key][2], questionedFeatureSet[key][2]))
                dist[key].append(
                    self.__distHamming([referenceFeatureSet[key][3]], [float(questionedFeatureSet[key][3])]))
                dist[key].append(
                    self.__distHamming([referenceFeatureSet[key][4]], [float(questionedFeatureSet[key][4])]))
                dist[key].append(
                    self.__distHamming([referenceFeatureSet[key][5]], [float(questionedFeatureSet[key][5])]))
        D.append(dist)

        dist = {}
        for key in referenceFeatureSet:
            if key in questionedFeatureSet:
                dist[key] = []
                dist[key].append(
                    self.__distSigmoid([referenceFeatureSet[key][0]], [float(questionedFeatureSet[key][0])]))
                dist[key].append(
                    self.__distSigmoid([referenceFeatureSet[key][1]], [float(questionedFeatureSet[key][1])]))
                dist[key].append(self.__distSigmoid(referenceFeatureSet[key][2], questionedFeatureSet[key][2]))
                dist[key].append(
                    self.__distSigmoid([referenceFeatureSet[key][3]], [float(questionedFeatureSet[key][3])]))
                dist[key].append(
                    self.__distSigmoid([referenceFeatureSet[key][4]], [float(questionedFeatureSet[key][4])]))
                dist[key].append(
                    self.__distSigmoid([referenceFeatureSet[key][5]], [float(questionedFeatureSet[key][5])]))
        D.append(dist)

        dist = {}
        for key in referenceFeatureSet:
            if key in questionedFeatureSet:
                dist[key] = []
                dist[key].append(
                    self.__distKLDivergence([referenceFeatureSet[key][0]], [float(questionedFeatureSet[key][0])]))
                dist[key].append(
                    self.__distKLDivergence([referenceFeatureSet[key][1]], [float(questionedFeatureSet[key][1])]))
                dist[key].append(self.__distKLDivergence(referenceFeatureSet[key][2], questionedFeatureSet[key][2]))
                dist[key].append(
                    self.__distKLDivergence([referenceFeatureSet[key][3]], [float(questionedFeatureSet[key][3])]))
                dist[key].append(
                    self.__distKLDivergence([referenceFeatureSet[key][4]], [float(questionedFeatureSet[key][4])]))
                dist[key].append(
                    self.__distKLDivergence([referenceFeatureSet[key][5]], [float(questionedFeatureSet[key][5])]))
        D.append(dist)

        return D

    def combine(self, distances, all_distances):
        # type: (list, list) -> list
        for i in range(len(distances)):
            all_distances[i][0].append(self.std(distances[i]))
            all_distances[i][1].append(self.__mean(distances[i]))
            all_distances[i][2].append(self.__median(distances[i]))
            all_distances[i][3].append(self.__max(distances[i]))
            all_distances[i][4].append(self.__min(distances[i]))

        return all_distances

    def std(self, distance):
        # type: (dict) -> list
        F = [[], [], [], [], [], []]

        for key in distance:
            for i in range(len(distance[key])):
                if i != 2:
                    F[i].append(float(distance[key][i]))
                else:
                    F[i].append(distance[key][i])

        for i in range((len(F[2]))):
            F[2][i] = (float(F[2][i][0]) + float(F[2][i][1]))/2

        for i in range(len(F)):
            print(F[i])
            F[i] = std(F[i])

        return F

    def __mean(self, distance):
        # type: (dict) -> list
        F = [[], [], [], [], [], []]

        for key in distance:
            for i in range(len(distance[key])):
                F[i].append(distance[key][i])

        for i in range(len(F)):
            F[i] = mean(F[i])

        return F

    def __median(self, distance):
        # type: (dict) -> list
        F = [[], [], [], [], [], []]

        for key in distance:
            for i in range(len(distance[key])):
                F[i].append(distance[key][i])

        for i in range(len(F)):
            F[i] = median(F[i])

        return F

    def __max(self, distance):
        # type: (dict) -> list
        F = [[], [], [], [], [], []]

        for key in distance:
            for i in range(len(distance[key])):
                F[i].append(distance[key][i])

        for i in range(len(F)):
            F[i] = max(F[i])

        return F

    def __min(self, distance):
        # type: (dict) -> list
        F = [[], [], [], [], [], []]

        for key in distance:
            for i in range(len(distance[key])):
                F[i].append(distance[key][i])

        for i in range(len(F)):
            F[i] = min(F[i])

        return F
