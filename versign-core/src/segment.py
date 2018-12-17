from sklearn.externals import joblib
from skimage.morphology import skeletonize

import cv2
import numpy as np
import remove_lines

def find_signatures(refSigns):
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
            signs.append((refSignsA[y:y+_h, x:x+_w], (x, y, _w, _h)))
            signs.append((refSignsB[y:y+_h, x:x+_w], (x, h/2 + y, _w, _h)))

    bounds = []
    for signature, oldBounds in signs:
        # Invert colors
        signature = cv2.bitwise_not(signature)

        # Approximate bounding box around signature
        points = np.argwhere(signature==0)      # find where the black pixels are
        points = np.fliplr(points)              # store them in x,y coordinates instead of row,col indices
        x, y, w, h = cv2.boundingRect(points)   # create a rectangle around those points
        x, y, w, h = x-10, y-10, w+20, h+20     # add padding
        _x, _y, _w, _h = oldBounds
        bounds.append((x + _x, y + _y, w, h))
    return bounds

def extract_signature(im, model):
    print 'Loading model'
    # Load the trained model
    clf = joblib.load(model)

    # crop bottom right of image where signature lies, according to our prior knowledge
    print 'Cropping cheque'
    w, h = im.shape
    im = im[w/2:w, int(0.60*h):h]
    w, h = im.shape

    # Thresholding to get binary image
    print 'Thresholding'
    thresh = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                   cv2.THRESH_BINARY_INV, 25, 30)

    # Remove lines from the image
    print 'Removing lines'
    thresh = remove_lines.remove(thresh, fill=True)

    # Perform component analysis
    print 'Finding connected components'
    connectivity = 8        # 4-way / 8-way connectivity
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)

    # Extract components
    for label in range(count):
        # Crop out the component
        x, y, w, h = stats[label, 0], stats[label, 1], stats[label, 2], stats[label, 3]
        component = thresh[y : y+h,
                           x : x+w]
       
        # The indexes of pixels belonging to char are stored in image
        im = np.where(labels==label)

        # Extract SURF features from the component
        surf = cv2.xfeatures2d.SURF_create()
        surf.setHessianThreshold(400)                       # using 400 Hessian threshold
        kp, des = surf.detectAndCompute(component, None)    # keypoints, descriptors

        if des is not None:
            # Classify each descriptor of the component (to build consensus)
            rows = des.shape[0]
            predictions = np.zeros(rows)
            for row in range(rows):
                predictions[row] = clf.predict(des[row].reshape(1,-1))
            
            # Component marked signature only if >99% sure
            votes_all = len(predictions)
            votes_yes = np.count_nonzero(predictions)
            confidence = 100.0 * votes_yes / votes_all
            if confidence < 1:
                thresh[im] = 0
        else:
            thresh[im] = 0

    # Invert colors
    thresh = cv2.bitwise_not(thresh)

    # Approximate bounding box around signature
    points = np.argwhere(thresh==0)         # find where the black pixels are
    points = np.fliplr(points)              # store them in x,y coordinates instead of row,col indices
    x, y, w, h = cv2.boundingRect(points)   # create a rectangle around those points
    x, y, w, h = x-10, y-10, w+20, h+20     # add padding
    
    # Crop out the signature
    cropped = thresh[y:y+h, x:x+w]
    points = np.argwhere(cropped==255)
    try:
        print 'Filling strokes'
        for point in points:
            try:
                y, x = point[0], point[1]
                tY, tX = point[0] + 1, point[1]
                bY, bX = point[0] - 1, point[1]
                lY, lX = point[0], point[1] + 1
                rY, rX = point[0], point[1] - 1

                if cropped[tY][tX] == 0 and cropped[bY][bX] == 0 and cropped[y][x] != 0:
                    cropped[y][x] = 0
                elif cropped[lY][lX] == 0 and cropped[rY][rX] == 0 and cropped[y][x] != 0:
                    cropped[y][x] = 0
            except:
                continue
    except:
        pass
    return center_inside(cropped)