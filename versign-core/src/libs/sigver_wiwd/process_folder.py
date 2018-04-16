""" This example extract features for all signatures in a folder,
    using the CNN trained on the GPDS dataset. Results are saved in a matlab
    format.

    Usage: python process_folder.py <signatures_path> <save_path>
                                    [canvas_size]

    Example:
    python process_folder.py signatures/ features/ models/signet.pkl

    This example will process all signatures in the "signatures" folder, using
    the SigNet model, and saving the resutls to the features folder

"""
from preprocess.normalize import preprocess_signature
from PIL import Image
import signet
from cnn_model import CNNModel
import numpy as np
import sys
import os
import scipy.io
from scipy.misc import imread

if __name__ == "__main__":
    if len(sys.argv) not in [3,5]:
        print('Usage: python process_folder.py <signatures_path> <save_path> '
              '[canvas_size]')
        print(sys.argv)
        exit(1)

    signatures_path = sys.argv[1]
    save_path = sys.argv[2]
    model_weight_path="models/signetf_lambda0.999.pkl"
    if len(sys.argv) == 3:
        canvas_size = (150, 220)  # Maximum signature size
    else:
        canvas_size = (int(sys.argv[3]), int(sys.argv[4]))

    print('Processing images from folder "%s" and saving to folder "%s"' % (signatures_path, save_path))
    print('Using model %s' % model_weight_path)
    print('Using canvas size: %s' % (canvas_size,))
    
    # Load the model
    extract_features(signatures_path, save_path, model_weight_path, canvas_size)

def extract_features(signatures_path, save_path, model_weight_path, canvas_size=(150, 220)):
    print('Processing images from folder "%s" and saving to folder "%s"' % (signatures_path, save_path))
    print('Using model %s' % model_weight_path)
    print('Using canvas size: %s' % (canvas_size,))

    model = CNNModel(signet, model_weight_path)
    files = os.listdir(signatures_path)

    # Note: it there is a large number of signatures to process, it is faster to
    # process them in batches (i.e. use "get_feature_vector_multiple")
    for f in files:
        if os.path.isdir(os.path.join(signatures_path, f)):
            extract_features(os.path.join(signatures_path, f), os.path.join(save_path, f), model, canvas_size)
            continue

        # Skip if file is not an image
        if f.split('.')[-1] not in ['jpg', 'png', 'tif']:
            continue
    
        # Load and pre-process the signature
        filename = os.path.join(signatures_path, f)
        original = imread(filename, flatten=1)
        #processed = preprocess_signature(original, canvas_size)
        #Image.fromarray(processed).show()

        # Use the CNN to extract features
        feature_vector = model.get_feature_vector(original)

        # Save in the matlab format
        save_filename = os.path.join(save_path, os.path.splitext(f)[0] + '.mat')
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        scipy.io.savemat(save_filename, {'feature_vector':feature_vector})