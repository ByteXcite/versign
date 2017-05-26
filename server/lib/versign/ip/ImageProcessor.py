from __future__ import print_function

from PIL import Image


class ImageProcessor:
    def __init__(self, image):
        self.signature = image
        self.processed = None

    def process(self):
        processed = self.signature.convert("L")

        print("\n\tThresholding image ... ", end="")
        threshold = self.__get_threshold(processed, (0, 0, processed.size[0], processed.size[1]))
        print("Done")

        print("\tBinarizing image ... ", end="")
        processed = self.__binarize(processed, threshold)
        print("Done")

        self.processed = processed

    def __get_threshold(self, image, bounds):
        # type: (Image, tuple) -> int
        min = 255
        max = 0
        for x in range(bounds[0], bounds[2]):
            for y in range(bounds[1], bounds[3]):
                p = image.getpixel((x, y))
                if p < min:
                    min = p

                if p > max:
                    max = p

        return (min + max) / 2

    def __binarize(self, image, threshold):
        # type: (int) -> None
        for x in range(0, image.size[0]):
            for y in range(0, image.size[1]):
                p = image.getpixel((x, y))

                if p > threshold:
                    p = 255
                else:
                    p = 0

                image.putpixel((x, y), p)

        return image
