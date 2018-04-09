#!/usr/bin/python

# This script is used to resize all the images (using bicubic interpolation)
# in a directory to a given size

import os, sys, errno
from scipy.misc import imresize, imsave
from scipy.misc import imread
import numpy as np
import cv2

# root = "/home/mmahad/Documents/FYP/jpg_to_mnist/training_images/"
# root = "/home/mmahad/datasets/my_dataset/test"
root = sys.argv[1]

def silentremove(filename):
    # This function deletes a file safely
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

def resize(rt):
    # This function resizes images in a directory
    for root, dirs, files in os.walk(rt):
        path = root
        for fil in files:
            print '.\t',
            data = imread(path+'/'+fil)
            f, e = os.path.splitext(path+'/'+fil)
            silentremove(path+'/'+fil)
            imsave(f+'.png', imresize(data,(250,250),interp='bicubic'))
            # silentremove(path+'/'+fil)

resize(root)
