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

    def writeTestResuls(self, variance, outfile):
        # type: (list, str) -> None
        # Create a new .csv file
        outfile = open(outfile + "-test.csv", "w")

        # Write header to the file
        header = "reference, questioned, ratio, transitions, centroid, blacks, normalized-size, inclination\n"
        outfile.write(header)

        # Write features row-by-row. Each row represents one cell in the image.
        for row in variance:
            line = ", , "
            for var in row:
                line += str(var) + ", "
            outfile.write(line[:-2] + "\n")

        # Close the output file
        outfile.close()
