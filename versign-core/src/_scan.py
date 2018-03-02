import subprocess
import os, errno, cv2

from preprocess import preprocess_sign

print "Press 1 to register new customer"
print "Press 2 to verify signatures of already enrolled customers"
choice  = raw_input()

def scanImg():
    bashCommand = "scanimage --resolution 10 --mode Gray --format tiff > document.tiff"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

if choice in ["1","2"]:
    if choice is '1':
        # if user pressed 1 i.e. to enroll new customer
        cnic  = raw_input("Enter CNIC number\t")
        # Create directory named cnic if not exists
        directory = "../db/users/" + cnic
        Dirs=[directory,directory+"/ref",directory+"/features",directory+"/temp"]

        try:
            for folder in Dirs:
                os.makedirs(folder)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        raw_input("Please put signature specimen paper in scanner and then hit [Enter]")
        # Scanner starts to scan image and saves to this path cnic/temp
        path = directory+"/temp/"+cnic+".tiff"
        # scanImg()

        im = cv2.imread("document.tiff", 0)
        # crop the original binary image to extract the connected components one by one
        # Syntax for cropping image as opencv image is numpy array
        #im = im[y:y+h,x:x+w]
        h, w = im.shape
        mx = w/2
        my = h/4
        padx = int(mx*0.10)
        pady = int(my*0.05)

        sigs = []
        for x in [0, mx]:
            for y in [0, my]:
                sigs.append(im[y+pady:y+my-2*pady, x+padx:x+mx-2*padx])

        i=0
        for sig in sigs:
            tempfile = Dirs[3]+"/T00" + str(i) + ".png"
            cv2.imwrite(tempfile, sig)

            i+=1
        
        os.system("python augment.py \"" + Dirs[3] + "\" \"" + Dirs[1] + "\"")
        os.system("python libs/sigver_wiwd/process_folder.py \"" + Dirs[1] + "\" \"" + Dirs[2] + "\" libs/sigver_wiwd/models/signet.pkl")
        # perform feature extraction
        # save features in fileName
        print "New user has been enrolled successfully"

    elif choice is '2':
        # if user selected 2 i.e. to verify the signatures of existing customer
        cnic = raw_input("Enter CNIC number\t")
        directory = "../db/users/" + cnic
        # Check if the user is already enrolled
        if os.path.isdir(directory):
            raw_input("Please put the bank check in scanner and then hit [Enter]")

            path = directory+"/"+cnic+".tiff"
            # Scanner starts to scan
            scanImg(path)
            # Verification module return the result as 0 or 1
            result = False
            if result is True:
                print "The questioned signature is genuine"
            else:
                print "The questioned signature is forged"
        else:
            print "This user is not currently enrolled in our system."
            print "Please select option 1 to enroll this cnic"
else:
    print "Please enter a number 1 or 2"
