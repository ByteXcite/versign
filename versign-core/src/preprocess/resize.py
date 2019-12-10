#!/usr/bin/python
# This script is used to resize all the images (using bicubic interpolation)
# in a directory to a given size

import os, sys
from scipy.misc import imresize
import numpy as np
import cv2

def resize_relative(image, canvas_size=(150, 220), interpolation="bilinear"):
    """Resizes an image to within specified width and height while
    preserving the aspect ratio.

    Keyword arguments:
    image -- image to be resized
    canvas_size -- maximum width and height of the image
    interpolation -- type of interpolation to use. (default 'bicubic')
    """
    W, H = canvas_size
    h, w = image.shape
    if H >= W:
        _w = W
        _h = int(float(h) / w * _w)

        if _h > H:
            _h = H
            _w = int(float(w) / h * _h)
    else:
        _h = H
        _w = int(float(w) / h * _h)
        if _w > W:
            _w = W
            _h = int(float(h) / w * _w)

    return imresize(image, (_h, _w), interp=interpolation)

def center_inside(image, canvas_size=(150, 220), interpolation="bilinear"):
    """
    Centers an image inside a canvas. Image is resized to fit
    on a white canvas while preserving the aspect ratio.

    Keyword arguments:
    image -- image to be resized
    canvas_size -- maximum width and height of the image
    interpolation -- type of interpolation to use. (default 'bicubic')
    """
    W, H = canvas_size
    canvas = np.ones(shape=(H, W)).astype('uint8')*255

    image = resize_relative(image, canvas_size, interpolation)
    h, w = image.shape
        
    xoff = (W-w) / 2
    yoff = (H-h) / 2

    
    canvas[yoff:yoff+h, xoff:xoff+w] = image
    return canvas

def batch_resize(root_dir, out_dir, canvas_size=(150, 220), interpolation="bilinear"):
    """
    This function resizes all images in a given directory, including
    its subfolders to given canvas size using specified interpolation
    method. Accepted image formats are PNG, JPG, TIFF, and BMP.

    Keyword arguments:
    root_dir -- dir in which images to be resized are located
    out_dir -- dir where resized images should be saved
    canvas_size -- maximum width and height of the image (default: (250,250))
    interpolation -- type of interpolation to use. (default: 'bicubic')
    """
    if not root_dir.endswith("/"):
        root_dir += "/"

    if not out_dir.endswith("/"):
        out_dir += "/"

    print "Processing", root_dir, "..."
    for path, dirs, files in os.walk(root_dir):
        print "Found", len(files), "files"
        for fn in files:
            infile = path + '/' + fn
            outfile = out_dir + path[len(root_dir):] + '/' + fn[:-4] + ".png"
            f, EXT = os.path.splitext(path + '/' + fn)
            if EXT.lower() in [".png", ".jpg", ".jpeg", ".tif", ".bmp"]:
                print "Processing", infile, "..."
                image = cv2.imread(infile, 0)
                ret, thresh = cv2.threshold(image, 0, 255, \
                                            cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                resized = center_inside(thresh, canvas_size, interpolation)
                if not os.path.exists(out_dir + path[len(root_dir):] + '/'):
                    os.makedirs(out_dir + path[len(root_dir):] + '/')
                cv2.imwrite(outfile, resized)
            else:
                print "Skipping", infile, "..."
                pass


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print "Invalid arguments"
        exit(-1)
    
    root = sys.argv[1]
    out = sys.argv[2]
    w = int(sys.argv[3])
    h = int(sys.argv[4])
    batch_resize(root, out, (w, h))