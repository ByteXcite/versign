# from skimage import io
import numpy as np

from PIL import Image


def convert_to_gray(rgb_image):
    return rgb_image.convert("L")


def smoothing(gray_image):
    pixels = []
    for x in range(0, gray_image.size[0] - 2, 2):
        row = []
        for y in range(0, gray_image.size[1] - 2, 2):
            p1 = gray_image.getpixel((x, y))
            p2 = gray_image.getpixel((x, y + 1))
            p3 = gray_image.getpixel((x, y + 2))
            p4 = gray_image.getpixel((x + 1, y))
            p5 = gray_image.getpixel((x + 1, y + 1))
            p6 = gray_image.getpixel((x + 1, y + 2))
            p7 = gray_image.getpixel((x + 2, y))
            p8 = gray_image.getpixel((x + 2, y + 1))
            p9 = gray_image.getpixel((x + 2, y + 2))

            row.append(np.median([p1, p2, p3, p4, p5, p5, p6, p7, p8, p9]))
        pixels.append(row)

    wd = len(pixels[0])
    ht = len(pixels)

    gray_image = gray_image.resize((wd, ht))

    for x in range(gray_image.size[0]):
        for y in range(gray_image.size[1]):
            xy = (x, y)
            value = (int(pixels[y][x]))
            gray_image.putpixel(xy, value)

    return gray_image


def remove_outliers(image, average):
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            p = image.getpixel((x, y))
            if p < average:
                image.putpixel((x, y), (average))

    return image


def average_intensity(smooth_image):
    # type: (Image, tuple) -> int
    min = 255
    max = 0
    for x in range(smooth_image.size[0]):
        for y in range(smooth_image.size[1]):
            p = smooth_image.getpixel((x, y))
            if p < min:
                min = p

            if p > max:
                max = p

    return (min + max) / 2


def make_binary(smooth_image, threshold):
    # type: (Image, int) -> Image
    for x in range(0, smooth_image.size[0]):
        for y in range(0, smooth_image.size[1]):
            p = smooth_image.getpixel((x, y))

            if p > threshold:
                p = 255
            else:
                p = 0

            smooth_image.putpixel((x, y), p)

    return smooth_image


def bounds_crop(binary_image):
    # type: (Image) -> Image
    """
    Locates bounding box of the signature in given signature image and crops the
    signature image at bounding box.

    :param binary_image: image to be cropped
    :return: cropped image
    """
    left, right, top, bottom = binary_image.size[0], 0, binary_image.size[1], 0
    for x in range(0, binary_image.size[0]):
        for y in range(0, binary_image.size[1]):
            p = binary_image.getpixel((x, y))

            if p < 128:
                if x < left:
                    left = x

                if x > right:
                    right = x

                if y < top:
                    top = y

                if y > bottom:
                    bottom = y

    return binary_image.crop((left, top, right, bottom))


def resize(cropped_image, width=800):
    # type: (Image) -> Image
    """
    Normalizes the size of signature images by resizing them with 800px witdh.
    Height is set such as to preserve the aspect ratio.

    :param cropped_image: image to be resize
    :return: resized image
    """
    height = int(float(cropped_image.size[1]) / cropped_image.size[0] * width)
    return cropped_image.resize((width, height))


def thin(smooth_image):
    # type: (Image, int) -> Image
    for y in range(0, smooth_image.size[1]):
        for x in range(1, smooth_image.size[0]):
            prev = smooth_image.getpixel((x - 1, y))
            this = smooth_image.getpixel((x, y))

            if prev > 0 >= this:
                smooth_image.putpixel((x, y), 0)
            else:
                smooth_image.putpixel((x, y), 255)

    return smooth_image


def thicken(image):
    # type: (Image) -> Image
    for x in range(1, image.size[0] - 1):
        for y in range(1, image.size[1] - 1):
            p = image.getpixel((x, y))

            tp = image.getpixel((x, y + 1))
            bm = image.getpixel((x, y - 1))
            rt = image.getpixel((x + 1, y))
            lt = image.getpixel((x - 1, y))

            if p != 0 and ((tp == 0 and bm == 0) or (lt == 0 and rt == 0)):
                image.putpixel((x, y), (0))

    return image


class ImageProcessor:
    def __get_pixel_matrix(self, image):
        pixels = []
        for x in range(image.size[0]):
            row = []
            for y in range(image.size[1]):
                p1 = image.getpixel((x, y))
                row.append(p1)

            pixels.append(row)

        return pixels

    def preprocess(self, image):
        # tmp = convert_to_gray(image)
        # avg = average_intensity(tmp)
        # tmp = remove_outliers(tmp, avg)

        # avg = average_intensity(tmp)
        # out = thicken(resize())

        out = resize(bounds_crop(image), 320)
        return out
