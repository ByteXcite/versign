from numpy import loadtxt


class FeatureReader:
    def importFromCSV(self, infile):
        # type: (str) -> dict
        """
        Reads the features from a given .csv file and populates a dictionary from them
        :param infile: name of input file (without extension)
        :return: dictionary of features imported from given file
        """
        features = {}

        data = loadtxt(infile, dtype=tuple, delimiter=":")
        for row in data[1:]:
            features[row[0]] = row[1][2:].split(", ")
            features[row[0]][2] = str(features[row[0]][2]).replace("(", "").replace(")", "").split("...")

        return features
