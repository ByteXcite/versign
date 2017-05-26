class KNNClassifier:
    def difference(self, referenceFeatureSet, questionedFeatureSet):
        # type: (dict, dict) -> dict
        difference = {}
        for key in referenceFeatureSet:
            if key in questionedFeatureSet:
                difference[key] = []
                difference[key].append(pow(float(referenceFeatureSet[key][0]) - float(questionedFeatureSet[key][0]), 2))
                difference[key].append(pow(float(referenceFeatureSet[key][1]) - float(questionedFeatureSet[key][1]), 2))
                difference[key].append(
                    pow(float(referenceFeatureSet[key][2][0]) - float(questionedFeatureSet[key][2][0]), 2)
                    + pow(float(referenceFeatureSet[key][2][1]) - float(questionedFeatureSet[key][2][1]), 2))
                difference[key].append(pow(float(referenceFeatureSet[key][3]) - float(questionedFeatureSet[key][3]), 2))
                difference[key].append(pow(float(referenceFeatureSet[key][4]) - float(questionedFeatureSet[key][4]), 2))
                difference[key].append(pow(float(referenceFeatureSet[key][5]) - float(questionedFeatureSet[key][5]), 2))

        return difference

    def variance(self, difference):
        # type: (dict) -> list
        SUM = [0, 0, 0, 0, 0, 0]
        for key in difference:
            SUM[0] += difference[key][0]
            SUM[1] += difference[key][1]
            SUM[2] += difference[key][2]
            SUM[3] += difference[key][3]
            SUM[4] += difference[key][4]
            SUM[5] += difference[key][5]

        AVG = []
        AVG.append(SUM[0] / 64)
        AVG.append(SUM[1] / 64)
        AVG.append(SUM[2] / 64)
        AVG.append(SUM[3] / 64)
        AVG.append(SUM[4] / 64)
        AVG.append(SUM[5] / 64)

        VAR = [0, 0, 0, 0, 0, 0]
        for key in difference:
            VAR[0] += pow(difference[key][0] - AVG[0], 2)
            VAR[1] += pow(difference[key][1] - AVG[1], 2)
            VAR[2] += pow(difference[key][2] - AVG[2], 2)
            VAR[3] += pow(difference[key][3] - AVG[3], 2)
            VAR[4] += pow(difference[key][4] - AVG[4], 2)
            VAR[5] += pow(difference[key][5] - AVG[5], 2)

        VAR[0] /= 64
        VAR[1] /= 64
        VAR[2] /= 64
        VAR[3] /= 64
        VAR[4] /= 64
        VAR[5] /= 64

        return VAR
