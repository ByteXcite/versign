#!/usr/bin/python
from libs.sigver_wiwd.preprocess.normalize import normalize_image
from PIL import Image
from scipy.misc import imread
from skimage.filters import threshold_otsu, threshold_local

import cv2
import numpy as np
import os


def resize(image, max_size=(800, 800)):
    # type: (Image) -> Image
    """
    Resizes an image to within specified width and height while
    preserving the aspect ratio.

    :param image: image to be resize
    :param max_size: maximum width and height of the image
    :return: resized image
    """
    wd, ht = image.size
    if wd >= ht:
        new_wd = max_size[0]
        new_ht = int(float(ht) / wd * new_wd)
    else:
        new_ht = max_size[1]
        new_wd = int(float(wd) / ht * new_ht)

    return image.resize((new_wd, new_ht))


def preprocess_sign(infile, outfile, canvas_size=(800, 800)):
    # type: (str) -> Image
    TMP = ".temp.png"
    
    # normalize signature's size
    resize(Image.open(infile)).save(TMP)

    # preprocess it
    arr = imread(TMP, flatten=1)
    proc = normalize_image(arr.astype(np.uint8), canvas_size)
    proc = normalize_image(proc.astype(np.uint8), canvas_size)
    Image.fromarray(proc).save(outfile)

def preprocess_cheque(infile, outfile):
    # Open image in grayscale mode
    image = np.array(Image.open(infile).convert("L"))

    # Apply local OTSU thresholding
    block_size = 25
    adaptive_thresh = threshold_local(image, block_size, offset=15)
    binarized = image > adaptive_thresh
    binarized = binarized.astype(float) * 255
    binarized = Image.fromarray(binarized).convert("L")

    # Save binarized file
    binarized.save(outfile)