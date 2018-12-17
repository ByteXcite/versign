import sys
rootDir = "../../versign-core/"
sys.path.append(rootDir)

from PIL import Image
from user_manager import register, is_registered
from verification import verify_cheque

import cv2
import errno
import subprocess
import os


def scanImage(outfile):
    bashCommand = "scanimage --resolution 10 --mode Gray --format tiff > " + outfile + ".tiff"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return outfile + ".tiff"

def onRegisterSelected():
    print "REGISTER NEW USER"
    userId = raw_input("User ID (must be unique): ")
    if is_registered(userId, dirCore=rootDir):
        print "ERROR. User already exists."
        return

    prompt = "Put signature specimen paper in scanner and hit [Enter]"
    raw_input(prompt)

    #filename = scanImage(outfile=userId)
    filename = "../res/004_SH1_G.png"

    refSigns = cv2.imread(filename, 0)

    h, w = refSigns.shape
    x = int(0.025*w)
    y = int(0.025*h)
    w = w - 2*x
    h = h - 2*y
    refSigns = refSigns[y:y+h, x:x+w]

    h, w = refSigns.shape
    if register(userId, refSigns, dirCore=rootDir):
        print "Enrollment successful"
    else:
        print "ERROR. User ID already exists."

def onVerifySelected():
    print "VERIFY SIGNATURE"
    userId = raw_input("User ID: ")
    if not is_registered(userId, dirCore=rootDir):
        print "ERROR. No such user."
        return

    prompt = "Put the bank cheque in scanner and hit [Enter]"
    raw_input(prompt)

    #filename = scanImage(outfile=userId)
    filename = "../res/sample_cheque_mahad.png"

    cheque = cv2.imread(filename, 0)
    result = verify_cheque(userId, cheque, dirCore=rootDir)
    if result is True:
        print "Verification Result: GENUINE"
    else:
        print "Verification Result: FORGED"

def main():
    print "VERSIGN: AUTOMATIC SIGNATURE VERIFICATION SYSTEM"
    options = ["1", "2", "0"]
    prompt = "\
    Select an option (0 to end):\n \
    \t1: Register new customer\n \
    \t2: Verify a signature\n \
    \t\t? "
    choice  = str(raw_input(prompt))
    while choice is not "0":
        if choice in options:
            if choice is "1":
                onRegisterSelected()
            elif choice is "2":
                onVerifySelected()
        else:
            print "Invalid choice. Please select again."
        choice  = str(raw_input(prompt))
    
if __name__ == "__main__":
    main()
