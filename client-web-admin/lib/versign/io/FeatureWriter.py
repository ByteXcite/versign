import os

class FeatureWriter:
    def exportToCSV(self, features, outfile):
        # type: (dict, str) -> None
        """
        Writes the features to a formatted .csv file
        :param features: dictionary of features for all cells in the signature image
        :param outfile: name of output file (without extension)
        :return: None
        """

        # Create a new .csv file
        outfile = open(outfile + ".csv", "w")

        # Write header to the file
        header = "cell:, ratio, transitions, centroid, blacks, normalized-size, inclination\n"
        outfile.write(header)

        # Write features row-by-row. Each row represents one cell in the image.
        for cell in features:
            row = cell + ":, "
            for feature in features[cell]:
                row += str(feature).replace(", ", "...") + ", "

            row = row[:-2] + "\n"
            outfile.write(row)

        # Close the output file
        outfile.close()

    def writeTestResuls(self, distances, outfilepath):
        # type: (list, str) -> None
        D = ["Euclidean", "Manhattan", "Hamming", "Sigmoid", "KLDivergence"]
        C = ["SD", "Mean", "Median", "Max", "Min"]

        for i in range(len(D)):
            for j in range(len(C)):
                if not os.path.isdir(outfilepath + "/" + D[i] + "/" + C[j] + "/"):
                    os.makedirs(outfilepath + "/" + D[i] + "/" + C[j] + "/")
                # Create a new .csv file
                outfile = open(outfilepath + "/" + D[i] + "/" + C[j] + "/distance.csv", "w")

                # Write header to the file
                header = "reference, questioned, ratio, transitions, centroid, blacks, normalized-size, inclination\n"
                outfile.write(header)

                # Write features row-by-row. Each row represents one cell in the image.
                q = 1
                for row in distances[i][j]:
                    line = outfilepath.split("/")[-1] + "," + str(q) + ", "
                    for var in row:
                        line += str(var) + ", "
                    q += 1
                    outfile.write(line[:-2] + "\n")

                # Close the output file
                outfile.close()
