#!/usr/bin/python

# This script is used to resize all the images (using bicubic interpolation)
# in a directory to a given size

import os, sys, errno
from scipy.misc import imresize, imsave
from scipy.misc import imread
import numpy as np
import cv2

def crop_bounds(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    retval, thresh_gray = cv2.threshold(gray, thresh=100, maxval=255, type=cv2.THRESH_BINARY)

    # find where the signature is and make a cropped region
    points = np.argwhere(thresh_gray==0) # find where the black pixels are
    points = np.fliplr(points) # store them in x,y coordinates instead of row,col indices
    x, y, w, h = cv2.boundingRect(points) # create a rectangle around those points
    x, y, w, h = x-10, y-10, w+20, h+20 # make the box a little bigger
    return image[y:y+h, x:x+w] # create a cropped region of the gray image

def resize(image, canvas_size, interpolation="bicubic"):
    """
    This image resizes one image to given canvas size using
    specified interpolation. Default is bicubic.
    """
    cropped = crop_bounds(image)
    return imresize(cropped, canvas_size, interp=interpolation)
    

def batch_resize(root_dir, canvas_size=(250, 250), interpolation="bicubic"):
    """
    This function resizes all images in a given directory, including
    its subfolders to given canvas size using specified interpolation
    method. Accepted image formats are PNG, JPG, TIFF, and BMP.

    Default canvas size is 250x250, and default interpolation method
    is bicubic.
    """
    for path, dirs, files in os.walk(root_dir):
        for fn in files:
            infile = path + '/' + fn
            outfile = infile
            f, EXT = os.path.splitext(path + '/' + fn)
            if EXT.lower() in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
                print "Processing", fn, "..."
                image = imread(infile)
                resized = resize(image, canvas_size, interpolation)
                imsave(outfile, resized)
            else:
                print "Skipping", fn, "..."

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Invalid arguments"
        exit(-1)
    
    root = sys.argv[1]
    batch_resize(root)