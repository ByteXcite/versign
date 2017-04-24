import os

from PIL import Image

from FeatureExtractor import FeatureExtractor
from FeatureSet import FeatureSet
from Person import Person
from Signature import Signature


def train(person, load, save):
    # type: (Person, str, str) -> None
    save += str(person.id) + "/"

    print "Training", person.name

    # If this person is not already registered, create his directory and profile
    if not os.path.isdir(save):
        os.makedirs(save)

        outfile = open(save + "person-info.txt", "w")
        outfile.write(str(person.id) + "\n")
        outfile.write(str(person.name) + "\n")
        outfile.close()

    # For each of the images in input directory
    allFeatures = []
    for image in os.listdir(load):
        if image.endswith('.jpg') or image.endswith('.png'):
            # Open image
            infile = load + image
            print "Signature:", infile
            sign = Image.open(infile)

            # Prepare signature
            signature = Signature(sign)
            signature.preprocess()

            # Extract feature set
            processed, features = FeatureExtractor().getFeatures(signature.processed)
            allFeatures.append(features)

            # Write feature set to files
            featureSet = ("ratio", "transitions", "centroid", "blacks", "normalized-size", "inclination", "angle-sum")
            outfiles = []

            for feature in featureSet:
                if not os.path.exists(save + feature):
                    os.mkdir(save + feature)

                outfiles.append(open(save + feature + "/" + image + ".txt", "w"))

            for key in features:
                outfiles[0].write(key + ": " + str(features[key][0]) + "\n")
                outfiles[1].write(key + ": " + str(features[key][1]) + "\n")
                outfiles[2].write(key + ": " + str(features[key][2]) + "\n")
                outfiles[3].write(key + ": " + str(features[key][3]) + "\n")
                outfiles[4].write(key + ": " + str(features[key][4]) + "\n")
                outfiles[5].write(key + ": " + str(features[key][5]) + "\n")

            for file in outfiles:
                file.close()

            # Write processed image to file
            outfile = save + image
            processed.save(outfile)

    # Stability analysis
    print "Calculatin average features ..."
    average = {}
    for key in allFeatures[0]:
        average[key] = [0, 0, [0, 0], 0, 0, 0]

    for features in allFeatures:
        for key in features:
            average[key][0] += features[key][0]
            average[key][1] += features[key][1]
            average[key][2][0] += features[key][2][0]
            average[key][2][1] += features[key][2][1]
            average[key][3] += features[key][3]
            average[key][4] += features[key][4]
            average[key][5] += features[key][5]

    for key in average:
        average[key][0] /= len(allFeatures)
        average[key][1] /= len(allFeatures)
        average[key][2][0] /= len(allFeatures)
        average[key][2][1] /= len(allFeatures)
        average[key][3] /= len(allFeatures)
        average[key][4] /= len(allFeatures)
        average[key][5] /= len(allFeatures)

    print "Writing average features ..."
    featureSet = ("ratio", "transitions", "centroid", "blacks", "normalized-size", "inclination", "angle-sum")
    outfiles = []

    for feature in featureSet:
        outfiles.append(open(save + feature + "/average.txt", "w"))

    for key in average:
        outfiles[0].write(key + ": " + str(average[key][0]) + "\n")
        outfiles[1].write(key + ": " + str(average[key][1]) + "\n")
        outfiles[2].write(key + ": " + str(average[key][2]) + "\n")
        outfiles[3].write(key + ": " + str(average[key][3]) + "\n")
        outfiles[4].write(key + ": " + str(average[key][4]) + "\n")
        outfiles[5].write(key + ": " + str(average[key][5]) + "\n")

    for file in outfiles:
        file.close()
