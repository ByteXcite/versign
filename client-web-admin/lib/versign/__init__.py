from __future__ import print_function

import os

import matplotlib.pyplot as plt
from PIL import Image
from numpy import loadtxt, mean as avg

from KNNClassifier import KNNClassifier
from versign.entity.Person import Person
from versign.io.FeatureReader import FeatureReader
from versign.io.FeatureWriter import FeatureWriter
from versign.ip.FeatureExtractor import FeatureExtractor
from versign.ip.ImageProcessor import ImageProcessor


class VerSign:
    def __init__(self, person):
        # type: (Person) -> None
        self.person = person

    def __features(self, infile):
        # type: (str) -> dict

        # Open signature image
        sign = Image.open(infile)

        # Prepare signature for feature extraction
        print("Preprocessing signature ... ", end="")
        signature = ImageProcessor(sign)
        signature.process()
        print("Done")

        # Extract feature set
        print("Extracting features ... ", end="")
        return FeatureExtractor().extract(signature.processed)

    def train(self):
        # type: (Person, str) -> None
        exporter = FeatureWriter()
        all_features = []

        # Extract features from each of the reference signatures
        for signature in os.listdir(self.person.refdir):
            if signature.endswith('.jpg') or signature.endswith('.png'):
                print("Training {} ...".format(signature))
                features = self.__features(self.person.refdir + signature)
                all_features.append(features)

                exporter.exportToCSV(features, self.person.outdir + signature[:-4])

    def test(self, testdir):
        # type: (str) -> None
        for ref_sign in os.listdir(self.person.outdir):
            if ref_sign.endswith('.csv') and ref_sign.startswith("R") and not ref_sign.endswith("test.csv"):
                print("Testing against reference {} ...".format(ref_sign))

                print("Reading reference signature data ... ", end="")
                ref_features = FeatureReader().importFromCSV(self.person.outdir + ref_sign)
                print("Done")

                comm_distances = [[[], [], [], [], []],
                                  [[], [], [], [], []],
                                  [[], [], [], [], []],
                                  [[], [], [], [], []],
                                  [[], [], [], [], []]]

                print("Questioned {} signatures. Test starting now ... ".format(str(len(os.listdir(testdir)))))
                for questioned_sign in os.listdir(testdir):
                    if questioned_sign.endswith('.jpg') or questioned_sign.endswith('.png'):
                        print("Testing: {} ...".format(questioned_sign))
                        if os.path.isfile(self.person.outdir + questioned_sign[:-4] + ".csv"):
                            questioned_features = FeatureReader().importFromCSV(
                                self.person.outdir + questioned_sign[:-4] + ".csv")
                        else:
                            questioned_features = self.__features(testdir + questioned_sign)
                            FeatureWriter().exportToCSV(questioned_features, self.person.outdir + questioned_sign[:-4])
                        print("\nDone")

                        knn = KNNClassifier()
                        print("Calculating distances ... ", end="")
                        distances = knn.distance(ref_features, questioned_features)
                        print("Done")

                        print("Combining distances of signature segments ... ", end="")
                        comm_distances = knn.combine(distances, comm_distances)
                        print("Done")

                print("Writing distances to file ... ", end="")
                FeatureWriter().writeTestResuls(comm_distances, self.person.outdir + ref_sign[:-4])
                print("Done")

    def plotReferenceFeatureHistograms(self):
        meanFeatures = [[], [], [], [], [], []]
        for referenceSignature in os.listdir(self.person.outdir):
            if referenceSignature.endswith('.csv') and referenceSignature.startswith("Q"):
                # Read features of reference signature
                referenceFeatures = FeatureReader().importFromCSV(self.person.outdir + referenceSignature)

                # Compute mean (by using an intermediate temporary representation)
                temp = KNNClassifier().std(referenceFeatures)
                #for key in referenceFeatures:
                #    temp[2] += (float(referenceFeatures[key][2][0]) + float(referenceFeatures[key][2][1]))/2
                #    for i in [0, 1, 3, 4, 5]:
                #        temp[i] += float(referenceFeatures[key][i])

                for i in range(6):
                    meanFeatures[i].append(temp[i])

        signatureSamples = range(len(meanFeatures[0]))

        FLabel = ["Aspect Ratio", "Black-to-White Transitions", "Centroid", "Black Pixels", "Normalized-Size",
                  "Centroid Inclination"]
        FColor = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

        for i in range(len(meanFeatures)):
            # plt.plot(signatureSamples, meanFeatures[i], c=FColor[i])

            GX = []
            DX = []
            FX = []

            GY = []
            DY = []
            FY = []

            for x in range(len(meanFeatures[i])):
                if x + 1 in [49, 52, 66]:
                    GX.append(meanFeatures[i][x])
                    GY.append(x + 1)
                elif x + 1 in [6, 15, 28, 29, 34, 87, 90]:
                    DX.append(meanFeatures[i][x])
                    DY.append(x + 1)
                else:
                    FX.append(meanFeatures[i][x])
                    FY.append(x + 1)
            plt.plot(GY, GX, 'o', c="g")
            plt.bar(GY, GX)
            plt.plot(DY, DX, 'o', c="b")
            plt.bar(DY, DX)
            plt.plot(FY, FX, 'o', c="r")
            plt.bar(FY, FX)
            # plt.plot(signatureSamples, meanFeatures[i], 'o', c=FColor[6])
            # plt.bar(signatureSamples, meanFeatures[i])
            plt.xlabel(FLabel[i])
            plt.savefig("Fig_Q" + FLabel[i] + ".png")
            plt.close()

    def plotCalculatedDistances(self, ref):
        D = ["Euclidean", "Manhattan", "Hamming", "Sigmoid", "KLDivergence"]
        C = ["SD", "Mean", "Median", "Max", "Min"]
        L = ["Aspect Ratio", "Black-to-White Transitions", "Centroid", "Black Pixels", "Normalized-Size", "Centroid Inclination"]

        for i in range(len(D)):
            for j in range(len(C)):
                infile = self.person.outdir + ref + "/" + D[i] + "/" + C[j] + "/distance.csv"
                data = loadtxt(infile, dtype=object, delimiter=", ")
                F = [[], [], [], [], [], []]
                for d in data[1:]:
                    for x in range(len(d) - 1):
                        F[x].append(float(d[x + 1]))

                for x in range(len(F)):
                    self.__plot_single(F[x], L[x], self.person.outdir + ref + "/" + D[i] + "/" + C[j] + "/" + L[x])

    def __plot_single(self, x, xlabel, outdir):
        y = range(100)
        self.__plot(x, y, xlabel, "Questioned Signatures", outdir)

    def __plot(self, x, y, xlabel, ylabel, outdir):
        xmax = max(x)

        for i in range(len(x)):
            if xmax == 0:
                x[i] /= 1
            else:
                x[i] /= xmax

        GX = []
        DX = []
        FX = []

        GY = []
        DY = []
        FY = []

        for i in range(len(x)):
            if i + 1 in [49, 52, 66]:
                GX.append(x[i])
                GY.append(y[i])
            elif i + 1 in [6, 15, 28, 29, 34, 87, 90]:
                DX.append(x[i])
                DY.append(y[i])
            else:
                FX.append(x[i])
                FY.append(y[i])
        plt.plot(GX, GY, 'o', c="g")
        plt.plot(DX, DY, 'o', c="b")
        plt.plot(FX, FY, 'o', c="r")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.savefig(outdir + ".png")
        plt.close()
