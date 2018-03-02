from sklearn.externals import joblib

import cv2
import numpy as np
import remove_lines

def extract_signature(filename, model):
    # Load the trained model
    clf = joblib.load(model)

    im = cv2.imread(filename, 0)

    # crop bottom right of image where signature lies, according to our prior knowledge
    w, h = im.shape
    im = im[w/2:w, int(0.60*h):h]
    w, h = im.shape

    # Thresholding to get binary image
    original = cv2.bitwise_not(im)
    smoothed = cv2.GaussianBlur(original, (35, 35), 0)
    cv2.subtract(original, smoothed, im)
    ret3, thresh = cv2.threshold(im, 0, 255, \
                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Remove lines from the image
    thresh = remove_lines.remove(thresh)

    # Perform component analysis
    connectivity = 4        # 4-way / 8-way connectivity
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
            #if confidence < 1:
            #    thresh[im] = 0
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
    return thresh[y:y+h, x:x+w]