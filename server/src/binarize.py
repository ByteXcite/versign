import argparse

parser = argparse.ArgumentParser(description='Applies OTSU thresholding on images.')
parser.add_argument("--file", dest="file", default=None, help="image file to binarize")
parser.add_argument("--dir", dest="folder", default=None, help="directory containing image files to binarize")
parser.add_argument("--sign", dest="sign", default=True, help="is this a signature? True = sign, False = cheque")

args = parser.parse_args()

if args.file == None and args.folder == None:
    args.file = "uploaded.png"
    Image.open(args.file).show()

from preprocess import *
import os

postfix = "_BIN.png"

def binarize(infile):
    outfile = infile[:-4] + postfix
    if args.sign:
        preprocess_sign(infile, outfile, (1024, 1024))
    else:
        preprocess_cheque(infile, outfile)

if args.folder == None:
    binarize(args.file)

else:
    if not args.folder.endswith("/"):
        args.folder += "/"

    extensions = ['jpg', 'bmp', 'png', 'gif']
    files = [fn for fn in os.listdir(args.folder)
             if any(fn.endswith(ext) and not fn.endswith(postfix) for ext in extensions)]
    
    for file in files:
        binarize(args.folder + file)