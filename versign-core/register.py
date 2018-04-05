#!/usr/local/bin/env python
import numpy as np
from PIL import Image

import os

fo = open("register/request.json", "r")
payload = fo.read()
fo.close()
# os.remove("register/request.json")

user = payload.split('customerID":"')[1].split('","refSignA')[0]
width = int(payload.split('width":')[1].split('}')[0])

pixelData = payload.split('pixelData":[')[1].split('],"width')[0].split(',')
for i in range(0, len(pixelData)):
    pixelData[i] = int(pixelData[i])
pixelData = [pixelData[i:i+width] for i in range(0, len(pixelData), width)]

image = Image.fromarray(np.array(pixelData).astype('uint8')).convert("L")

image = np.array(image)
print "Converted to numpy array"

from skimage.filters import threshold_local
print "Imported thresholder"

# Apply local OTSU thresholding
block_size = 25
adaptive_thresh = threshold_local(image, block_size, offset=15)
print "Calculated adaptive threshold"

binarized = image > adaptive_thresh
print "Binarized image"

binarized = binarized.astype(float) * 255
binarized = Image.fromarray(binarized).convert("L")
print "Converted back to image"

# Save binarized file
binarized.save("register/" + user + ".png")
print "Saved binarized image"