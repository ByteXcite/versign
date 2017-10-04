#########################################################################################
# This script takes two arguments, inDir and outDir, and augments the input data in     #
# inDir by generating four new images for each image in the input data. Augmentation is #
# performed by performing minor transformations (rotation, etc.) on input data.         #
#########################################################################################
from CertSign import ImageProcessor
from PIL import Image

import cv2, random, os, numpy as np, sys


def otsu(image):
    blur = cv2.GaussianBlur(image, (5,5), 0)
    ret, bin = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return bin

def randomRotate(image, min=-5, max=5):
    im2 = image.convert("RGBA")
    rot = im2.rotate(random.uniform(min, max), expand=True)
    fff = Image.new("RGBA", rot.size, (255,)*4)
    out = Image.composite(rot, fff, rot)
    return out.convert(image.mode)

def main():
    # Validate command-line arguments
    if len(sys.argv) < 3:
        print "\nUsage:\tpython", sys.argv[0], "<input-folder> <output-folder>\n"
        return

    # Path of input directory
    inDir = sys.argv[1]
    if not inDir.endswith("/"):
        inDir += "/"

    # Path where augmented data will be saved
    outDir = sys.argv[2]
    if not outDir.endswith("/"):
        outDir += "/"

    # No. of copies of to create
    copies = 4

    # Max angle to rotate through
    aMax = 5

    # For each image file in the input directory
    for file in os.listdir(inDir):
        if not file.endswith(".jpg") and not file.endswith(".png"):   # Ignore non-images
            continue

        # Extract file name and extension
        fn = file[:-4]
        ext = "." + file.split(".")[-1]
        print fn, ext

        # Apply OTSU thresholding on input image and save it
        outFile = outDir + fn + ".0" + ext
        cv2.imwrite(outFile, otsu(cv2.imread(inDir +  fn + ext, 0)))

        # Crop and normalize image's size
        cropped = ImageProcessor().preprocess(Image.open(outFile).convert("L"))
        cropped.save(outFile)

        # Augment input data by rotating image at random angles in range (-5, 5)
        image = Image.open(outFile)
        for i in range(0, copies):
            rotated = randomRotate(image, min=-aMax, max=aMax)
            rotated.save(outDir + fn + "." + str(i + 1) + ext)

main()