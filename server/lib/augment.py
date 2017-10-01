from PIL import Image
import numpy as np
import cv2

import random
import os

# os.system("process_folder.py ../data/MyData/Forged/ ../features/MyData/Questioned models/signet.pkl")

def otsu(image):
    blur = cv2.GaussianBlur(image, (5,5), 0)
    ret, bin = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return bin

def rotate_random(image, min=-5, max=5):
    im2 = image.convert("RGBA")
    rot = im2.rotate(random.uniform(min, max), expand=True)
    fff = Image.new("RGBA", rot.size, (255,)*4)
    out = Image.composite(rot, fff, rot)
    return out.convert(image.mode)

def save_rotated(img, file, postfix, type=".png"):
    path = file + "." + str(postfix) + type
    print path
    img.save(path)

dir = "data/MyData/Forged/"
input_data = ["F001", "F002", "F003", "F004"]
type = ".jpg"

n = 0.0
for i in input_data:
    n += 1.0

    # Open the signature image and apply OTSU thresholding
    image = cv2.imread(dir + i + type, 0)
    b_img = otsu(image)

    # Save binary signature image
    out_file = dir + i + ".0" + type
    cv2.imwrite(out_file, b_img)
    
    # Augment input signature by creating seven copies
    # rotated at random angles in range (-5, 5)
    b_img = Image.open(out_file)
    for j in range(1, 7):
        rotated = rotate_random(b_img, min=-5, max=5)
        save_rotated(rotated, dir + i, j)