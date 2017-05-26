from __future__ import print_function

import os

from PIL import Image

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
            if ref_sign.endswith('.csv') and ref_sign.startswith("R"):
                print("Testing against reference {} ...".format(ref_sign))

                print("Reading reference signature data ... ", end="")
                ref_features = FeatureReader().importFromCSV(self.person.outdir + ref_sign)
                print("Done")

                variance = []
                print("Questioned {} signatures. Test starting now ... ".format(str(len(os.listdir(testdir)))))
                for questioned_sign in os.listdir(testdir):
                    if questioned_sign.endswith('.jpg') or questioned_sign.endswith('.png'):
                        print("Testing: {} ...".format(questioned_sign))
                        questioned_features = self.__features(testdir + questioned_sign)
                        print("\nDone")

                        knn = KNNClassifier()
                        print("Calculating difference ... ", end="")
                        feature_difference = knn.difference(ref_features, questioned_features)
                        print("Done")

                        print("Getting variance ... ", end="")
                        variance.append(knn.variance(feature_difference))
                        print("Done")

                print("Writing variance to file ... ", end="")
                FeatureWriter().writeTestResuls(variance, self.person.outdir + ref_sign[:-4])
                print("Done")
