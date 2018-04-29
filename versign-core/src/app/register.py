#!/usr/local/bin/env python
import numpy as np
from PIL import Image

import json
import os

# Read input data from JSON
fn = "../../../versign-core/src/app/register_request.json"
fo = open(fn, "r")
payload = json.loads(fo.read())
fo.close()
os.remove(fn)

# Get customer ID
user = payload['customerId']
print 'Customer:', user

# Extract all four reference signatures
refSigns = [payload['refSignA'], payload['refSignB'], payload['refSignC'], payload['refSignD']]
signImages = []
index = 0
for refSign in refSigns:
    pixelData = np.array(refSign['pixelData']).astype('uint8')
    width = refSign['width']
    height = refSign['height']

    a = np.reshape(pixelData, (height, width))

    Image.fromarray(a).save("../../../versign-core/src/app/register_" + user + "_" + str(index) + ".png")
    index += 1