#!/usr/bin/env python
import numpy as np
from PIL import Image

import os

fo = open("log.json", "r")
payload = fo.read()
fo.close()

os.remove("log.json")

width = int(payload.split('width":')[1].split('}')[0])

pixelData = payload.split('pixelData":[')[1].split('],"width')[0].split(',')
for i in range(0, len(pixelData)):
    pixelData[i] = int(pixelData[i])
pixelData = [pixelData[i:i+width] for i in range(0, len(pixelData), width)]

Image.fromarray(np.array(pixelData).astype('uint8')).save("uploaded.png")