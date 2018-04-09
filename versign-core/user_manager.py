from src.augment import augment
from src.libs.sigver_wiwd.process_folder import extract_features

import cv2
import numpy as np
import os
import remove_lines
import shutil


def is_registered(userId, dbPath="db/users/", dirCore=""):
    """
    Returns true if the specified user is already registered with
    the system, false otherwise.

    Keyword arguments:
    userId -- identifier of the user to check
    dbPath   -- relative path of users database (default: 'db/users/')
    dirCore  -- relative path of API's root directory (default: '')
    """
    dirRoot = dirCore + dbPath + userId + "/"
    return os.path.exists(dirRoot)

def register(userId, refSigns, dbPath="db/users/", dirCore=""):
    """
    Registers a new user with the system, if no user with given
    user ID already exists.

    Returns a boolean indicating whether the registration was
    sucessful or not.
    
    Keyword arguments:
    userId   -- a unique string identifying the new user.
    refSigns -- an numpy array containing image of four reference
                signatures of the user in a grid.
    dbPath   -- relative path of users database (default: 'db/users/')
    dirCore  -- relative path of API's root directory (default: '')
    """
    dirRoot = dirCore + dbPath + userId + "/"
    if is_registered(userId, dbPath, dirCore):
        return False

    # Create required directories for new user
    dirTemp = dirRoot + "temp/"
    os.makedirs(dirTemp)

    dirImages = dirRoot + "images/"
    os.makedirs(dirImages)

    dirFeatures = dirRoot + "features/"
    os.makedirs(dirFeatures)

    # Thresholding to get binary image
    original = cv2.bitwise_not(refSigns)
    smoothed = cv2.GaussianBlur(original, (35, 35), 0)
    cv2.subtract(original, smoothed, refSigns)
    ret3, thresh = cv2.threshold(refSigns, 0, 255, \
                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Remove grid lines from the image
    refSigns = remove_lines.remove(thresh)

    # Divide 4x2 grid into two 2x2 grids
    h, w = refSigns.shape
    refSignsA = refSigns[0:h/2, 0:w]
    refSignsB = refSigns[h/2:h, 0:w]

    # Extract all eight signatures from the grid
    _h, _w = np.array(refSignsA.shape) / 2
    py, px = int(_h * 0.05), int(_w * 0.05)

    _h, _w = _h - 2*py, _w - 2*px

    signs = []
    for x in [px, _w]:
        for y in [py, _h]:
            signs.append(refSignsA[y:y+_h, x:x+_w])
            signs.append(refSignsB[y:y+_h, x:x+_w])

    print len(signs)

    # TODO: Preprocess signature images

    # Save these four signatures in a temporary directory
    PREFIX = "R"
    EXT = ".png"
    index=0
    for signature in signs:
        # Invert colors
        signature = cv2.bitwise_not(signature)

        # Approximate bounding box around signature
        points = np.argwhere(signature==0)      # find where the black pixels are
        points = np.fliplr(points)              # store them in x,y coordinates instead of row,col indices
        x, y, w, h = cv2.boundingRect(points)   # create a rectangle around those points
        x, y, w, h = x-10, y-10, w+20, h+20     # add padding
    
        # Crop out the signature
        signature = signature[y:y+h, x:x+w]
        
        outfile = dirTemp + PREFIX + str(index) + EXT
        cv2.imwrite(outfile, signature)
        index+=1

    # Use data augmentation to generate more samples
    augment(dirTemp, dirImages)

    # Delete temporary files
    shutil.rmtree(dirTemp)

    # Extract features from reference signatures
    extract_features(dirImages, dirFeatures, dirCore + "src/libs/sigver_wiwd/models/signet.pkl")
    return True

def unregister(userId):
    """
    Removes an existing user from system database.

    Keyword arguments:
    userId -- identifier of the user to remove
    """
    dirRoot = "db/users/" + userId + "/"
    if os.path.exists(dirRoot):
        shutil.rmtree(dirRoot)