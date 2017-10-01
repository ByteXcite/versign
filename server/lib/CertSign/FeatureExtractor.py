from math import atan

import numpy as np
import scipy.stats as stat
from PIL import Image


class FeatureExtractor:
    def __feature_set_one(self, signature_image, bounds):
        # type: (Image, tuple) -> tuple
        """
        Extracts the number of black to white transitions, number of black pixels,
        centroid, centroid inclination and black pixels' average inclination in
        the signature image within the defined boundaries.

        A black-to-white transition is counted when a white pixel is encountered in
        immediate neighbourhood of a black pixel when traversing the image from top
        left corner to bottom right.

        A black pixel has intensity 0. Centroid is weighted center of the black pixels
        signature image. Inclination is defined as the angle a point makes with
        bottom-left corner of the image region.

        :param signature_image: signature image
        :param bounds: boundary (left, right, top, bottom) within which features are
                       to be extracted

        :return: list containing # of transitions, # of black, centroid, centroid
                 inclination and average inclination
        """
        black_pixel_count = 0
        transition_count = 0
        average_inclination = 0
        centroid = [0, 0]
        prev_pixel = signature_image.getpixel((bounds[0], bounds[2]))
        for x in range(int(bounds[0]) + 1, int(bounds[1])):
            for y in range(int(bounds[2]) + 1, int(bounds[3])):
                # Count black pixels, their positions and inclination
                if signature_image.getpixel((x, y)) == 0:
                    black_pixel_count += 1
                    centroid[0] += x
                    centroid[1] += y

                    dx = (float)(centroid[0] - bounds[0])
                    dy = (float)(bounds[3] - centroid[1])
                    if dx != 0:
                        average_inclination = atan(dy / dx)
                    else:
                        average_inclination = 0

                # Count transitions
                curr_pixel = signature_image.getpixel((x, y))
                if curr_pixel == 255 and prev_pixel == 0:
                    transition_count += 1

                prev_pixel = curr_pixel

        # Compute centroid. If image has no blacks inside the specified bounds,
        # set centroid to middle of the bounded region.
        if black_pixel_count == 0:
            centroid = [float(bounds[0] + bounds[1]) / 2, float(bounds[2] + bounds[3]) / 2]
        else:
            centroid = centroid[0] / black_pixel_count, centroid[1] / black_pixel_count

        # Compute inclinations
        if black_pixel_count == 0:
            average_inclination = 0
        else:
            average_inclination /= black_pixel_count

        dx = (float)(centroid[0] - bounds[0])
        dy = (float)(bounds[3] - centroid[1])
        if dx != 0:
            centroid_inclination = atan(dy / dx)
        else:
            centroid_inclination = 0

        return transition_count, black_pixel_count, centroid, centroid_inclination, average_inclination

    def __feature_set_two(self, bounds, black_pixels):
        # type: (tuple, int) -> tuple
        """
        Computes aspect ratio of a bounded region of an image, and its normalized
        size.

        Aspect ratio is defined as ratio of width to height. Normalized size is the
        ratio of product of dimensions and black pixel count. -1 indicates infinity
        in each case.

        :param bounds: boundaries (left, right, top, bottom) of the image region
        :return: list containing aspect ratio, normalized-size
        """
        width = (float)(bounds[1] - bounds[0])
        height = (float)(bounds[3] - bounds[2])

        if height == 0:
            ratio = -1.0
        else:
            ratio = width / height

        if black_pixels != 0:
            nsize = width * height / black_pixels
        else:
            nsize = -1

        return ratio, nsize

    def __feature_set_three(self, signature_image):
        P = []
        for x in range(0, signature_image.size[0]):
            for y in range(0, signature_image.size[1]):
                P.append(signature_image.getpixel((x, y)))
        P = np.array(P)
        deviation = np.std(P)
        kurtosis = stat.kurtosis(P)
        skewness = stat.skew(P)

        return deviation, kurtosis, skewness

    def __extract_split_features(self, signature_image, bounds, depth=0):
        # type: (Image, tuple, int) -> None
        transitions, blacks, centroid, angle, avg_angle = self.__feature_set_one(signature_image, bounds)

        if depth < 3 and centroid != 0:
            self.__extract_split_features(signature_image, (bounds[0], centroid[0], bounds[2], centroid[1]), depth + 1)
            self.__extract_split_features(signature_image, (centroid[0], bounds[1], bounds[2], centroid[1]), depth + 1)
            self.__extract_split_features(signature_image, (bounds[0], centroid[0], centroid[1], bounds[3]), depth + 1)
            self.__extract_split_features(signature_image, (centroid[0], bounds[1], centroid[1], bounds[3]), depth + 1)
        else:
            ratio, nsize = self.__feature_set_two(bounds, blacks)

            self.__features[0].append(ratio)
            self.__features[1].append(blacks)
            self.__features[2].append(avg_angle)
            self.__features[3].append(centroid[0])
            self.__features[4].append(centroid[1])
            self.__features[5].append(angle)
            self.__features[7].append(nsize)
            self.__features[10].append(transitions)

    def __merge_split_features(self, image):
        # type: () -> None
        self.__features[0] = np.std(self.__features[0])
        self.__features[1] = np.sum(self.__features[1])
        self.__features[2] = np.std(self.__features[2])
        self.__features[3] = np.std(self.__features[3])
        self.__features[4] = np.std(self.__features[4])
        self.__features[5] = np.std(self.__features[5])
        self.__features[7] = np.std(self.__features[7])
        self.__features[10] = np.std(self.__features[10])

        self.__features[6], self.__features[8], self.__features[9] = self.__feature_set_three(image)

    def extract_features(self, signature_image):
        self.__features = [[],  # 0 Aspect ratio
                           [],  # 1 Black pixel count
                           [],  # 2 Black pixel average inclination
                           [],  # 3 CentroidX
                           [],  # 4 CentroidY
                           [],  # 5 Centroid inclination
                           [],  # 6 Kurtosis
                           [],  # 7 Normalized size
                           [],  # 8 Skewness
                           [],  # 9 Standard deviation
                           []]  # 10 Transitions
        self.__extract_split_features(signature_image,
                                      (0, signature_image.size[0],
                                       0, signature_image.size[1]))
        self.__merge_split_features(signature_image)
        return self.__features
