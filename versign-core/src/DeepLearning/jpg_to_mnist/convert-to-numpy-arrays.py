import numpy as np
import os
import cv2
list_of_imgs = []
img_dir = "/home/mmahad/Documents/FYP/versign/versign-core/src/DeepLearning/jpg_to_mnist/training_images/1/"
for img in os.listdir(img_dir):
    img = os.path.join(img_dir, img)
    if not img.endswith(".png"):
        continue
    a = cv2.imread(img)
    print a.shape
    if a is None:
        print "Unable to read image", img
        continue
    list_of_imgs.append(a.flatten())
train_data = np.array(list_of_imgs)
print train_data.shape
