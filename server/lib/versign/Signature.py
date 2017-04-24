from PIL import Image


class Signature:
    def __init__(self, image):
        self.signature = image
        self.processed = None

    def preprocess(self):
        processed = self.signature.convert("L")

        threshold = self.__calculateThreshold(processed)
        processed = self.__makeBinary(processed, threshold)

        self.processed = processed

    def __calculateLocalThreshold(self, image, bounds):
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

    def __calculateThreshold(self, image):
        # type: (Image) -> int
        bounds = (0, 0, image.size[0], image.size[1])
        return self.__calculateLocalThreshold(image, bounds)

    def __makeBinary(self, image, threshold):
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
