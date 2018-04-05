import subprocess

class ScannerError(IOError):
    def __init__(self):
        super.__init__()

def scanImage(outfile):
    """
    Gets an image from a connected scanning device and saves it
    in a TIFF file at specified location.
    
    Throws a ScannerError if there is an error reading from the
    scanning device.

    Keyword arguments:
    outfile -- complete path of file where image should be saved
    """
    try:
        outfile = outfile + ".tiff"
        bashCommand = "scanimage --resolution 10 --mode Gray --format tiff > '" + outfile + "'"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    except:
        raise ScannerError()