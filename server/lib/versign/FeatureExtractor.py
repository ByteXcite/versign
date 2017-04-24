from math import atan

from PIL import Image, ImageDraw


class FeatureExtractor:
    def __init__(self):
        self.features = {}

    def __getCentroid(self, image, bounds):
        """
        For the section of image inside the given boundaries, this method calculates and
        returns the centroid, number of black pixels, and normalized sum of inclination
        angles.

        :param image: PIL image from which features are to be extracted
        :param bounds: coordinates (left, right, top, bottom) from which to extract features
        :return: (centroid, black-pixels, inclination-sum)
        """
        XX, YY = 0, 0
        blacks = 0
        angles = 0
        transitions = 0

        prev = image.getpixel((bounds[0], bounds[2]))
        for x in range(bounds[0], bounds[1]):
            for y in range(bounds[2], bounds[3]):
                curr = image.getpixel((x, y))
                if curr == 255 and prev == 0:
                    transitions += 1
                prev = curr

                if image.getpixel((x, y)) == 0:
                    XX += x
                    YY += y

                    blacks += 1

                    # Summation of angles
                    dx = (float)(x - bounds[0])
                    dy = (float)(bounds[3] - y)
                    if dx != 0:
                        angles += atan(dy / dx)

        if blacks != 0:
            XX /= blacks
            YY /= blacks
            angles /= blacks

        else:
            XX = (bounds[0] + bounds[1]) / 2
            YY = (bounds[2] + bounds[3]) / 3

        return (XX, YY), blacks, angles, transitions

    def __boundingBox(self, image):
        left, right, top, bottom = image.size[0], 0, image.size[1], 0

        # Calculate bounds
        for x in range(0, image.size[0]):
            for y in range(0, image.size[1]):
                p = image.getpixel((x, y))

                if p < 128:
                    if x < left:
                        left = x

                    if x > right:
                        right = x

                    if y < top:
                        top = y

                    if y > bottom:
                        bottom = y

        return left, right, top, bottom

    def __extractFeatures(self, image, bounds, segment="", depth=0):
        # Find centroid
        centroid, blacks, angles, transitions = self.__getCentroid(image, bounds)

        if depth < 3 and centroid != 0:
            image = self.__extractFeatures(image, (bounds[0], centroid[0], bounds[2], centroid[1]), segment + "1",
                                           depth + 1)
            image = self.__extractFeatures(image, (centroid[0], bounds[1], bounds[2], centroid[1]), segment + "2",
                                           depth + 1)
            image = self.__extractFeatures(image, (bounds[0], centroid[0], centroid[1], bounds[3]), segment + "3",
                                           depth + 1)
            image = self.__extractFeatures(image, (centroid[0], bounds[1], centroid[1], bounds[3]), segment + "4",
                                           depth + 1)
        else:
            # Calculate aspect ratio
            width = (float)(bounds[1] - bounds[0])
            height = (float)(bounds[3] - bounds[2])

            if height == 0:
                ratio = 0
            else:
                ratio = round(width / height, 2)

            # Calculate normalized size
            if blacks != 0:
                nsize = width * height / blacks
            else:
                nsize = 0

            # Calculate angle of inclination
            dx = (float)(centroid[0] - bounds[0])
            dy = (float)(bounds[3] - centroid[1])
            if dx != 0:
                angle = atan(dy / dx)
            else:
                angle = 0

            # Draw bounding box
            image = self.__drawBox(image, bounds, centroid)

            # Return features
            self.features[segment] = (ratio, transitions, centroid, blacks, nsize, angle, angles)
            return image

        return image

    def __drawBox(self, image, bounds, centroid):
        # type: (Image, tuple) -> Image
        left, right, top, bottom = bounds
        # Draw bounds on the image
        for x in range(left, right):
            image.putpixel((x, top), 0)
            image.putpixel((x, bottom - 1), 0)

        for y in range(top, bottom):
            image.putpixel((left, y), 0)
            image.putpixel((right - 1, y), 0)

        draw = ImageDraw.Draw(image)
        draw.line((bounds[0], bounds[3], centroid[0], centroid[1]), fill=128)

        return image

    def getFeatures(self, image):
        # type: (Image) -> (Image, dict)
        # Locate bounding box
        box = self.__boundingBox(image)
        image = image.crop((box[0], box[2], box[1] - box[0], box[3] - box[2]))
        size = image.size
        size = (2048, int(float(size[1]) / size[0] * 2048))
        image = image.resize(size)

        # Extract features
        self.features = {}
        image = self.__extractFeatures(image, (0, image.size[0], 0, image.size[1]))

        return image, self.features
