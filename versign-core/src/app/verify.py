#!/usr/local/bin/env python
from PIL import Image

import cv2
import numpy as np
import os

fo = open("verisign-core/bin/verify/request.json", "r")
payload = fo.read()
fo.close()
os.remove("verisign-core/bin/verify/request.json")

user = payload.split('customerId":"')[1].split('","questionedSignature')[0]
width = int(payload.split('width":')[1].split('}')[0])

pixelData = payload.split('pixelData":[')[1].split('],"width')[0].split(',')
for i in range(0, len(pixelData)):
    pixelData[i] = int(pixelData[i])
pixelData = [pixelData[i:i+width] for i in range(0, len(pixelData), width)]

filename = "verisign-core/bin/verify/" + user + ".png"

image = Image.fromarray(np.array(pixelData).astype('uint8')).convert("L")
image.save(filename)

im = cv2.imread(filename, 0)
w, h = im.shape

# Otsu's thresholding after Gaussian filtering
blur = cv2.GaussianBlur(im, (5,5), 0)
ret3, binarized = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
print "Binarized image"

# Save binarized file
cv2.imwrite(filename, binarized)
print "Saved binarized image"