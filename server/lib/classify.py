import scipy.io as spy
import os
import numpy as np
import matplotlib.pyplot as plt


def save_plot(predictions, xlabel="Signature", ylabel="Prediction", title=""):
    GX = [49, 52, 66]
    GY = []

    DX = [6, 15, 28, 29, 34, 87, 90]
    DY = []

    FX = []
    FY = []
    for i in range(len(predictions)):
        if i + 1 in GX:
            GY.append(predictions[i])
        elif i + 1 in DX:
            DY.append(predictions[i])
        else:
            FX.append(i + 1)
            FY.append(predictions[i])

    plt.plot(FX, FY, 'o', c='r')
    plt.plot(GX, GY, 'o', c='g')
    plt.plot(DX, DY, 'o', c='b')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(title)
    plt.close()


# Create an empty feature array
features = []

# Populate feature array from extracted data
features_path = "features/4NSigComp2010/TestSet/Questioned/"
for f in os.listdir(features_path):
    if not f.endswith(".mat"):
        continue
    else:
        features.append(list(spy.loadmat(features_path + f)['feature_vector'][0]))

# Convert features to a numpy array
features = np.array(features)

# Save plots for each of the individual features
for i in range(2048):
    save_plot(features[:, [i]], title="features/4NSigComp2010/TestSet/Questioned/visuals/Feature No. " + str(i) + ".png")
