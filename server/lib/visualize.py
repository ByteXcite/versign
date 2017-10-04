############################################################################################
# This script takes two arguments, inDir and outDir, and reads features from .mat files in #
# input directory and plots each feature on graph and saves them in output directory.      #
############################################################################################
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.io as spy

def subplot(x, Y, s='o', c='r'):
    plt.plot(x, Y, s, c=c)

def plot(predictions, title, xlabel="x", ylabel="Y"):
    x_real = [49, 52, 66, 6, 15, 28, 29, 34, 87, 90]
    Y_real = []

    x_forg = []
    Y_forg = []
    for i in range(len(predictions)):
        if i+1 in x_real:
            Y_real.append(predictions[i])
        else:
            x_forg.append(i+1)
            Y_forg.append(predictions[i])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    subplot(x_real, Y_real, 'o', 'g')
    subplot(x_forg, Y_forg, 'x', 'r')
    
    plt.savefig(title)
    plt.close()

def main():
    # Validate command-line arguments
    if len(sys.argv) < 3:
        print "\nUsage:\tpython", sys.argv[0], "<input-folder> <output-folder>\n"
        return

    # Path of input directory
    inDir = sys.argv[1]
    if not inDir.endswith("/"):
        inDir += "/"

    # Path where augmented data will be saved
    outDir = sys.argv[2]
    if not outDir.endswith("/"):
        outDir += "/"

    images = []
    # For each .mat file in the input directory
    for fn in os.listdir(inDir):
        if not fn.endswith(".mat"): # Ignore irrelevant files
            continue

        # Read features from current file
        features = spy.loadmat(inDir + fn)['feature_vector'][0]
        images.append(list(features))

    # Save plots for each of the individual features
    for i in range(len(images[0])):
        plot(images[:, [i]], outDir + "F" + str(i+1) + ".png")