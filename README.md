# VerSign: An Off-Line Signature Verification System

A complete system to detect frauds using forged signatures.

## Dependencies
### Python
#### Image Processing
- [OpenCV](https://pypi.org/project/opencv-python/)
- [Python Image Library (PIL)](https://pillow.readthedocs.io/en/5.1.x/installation.html)
- [Scikit-Image](http://scikit-image.org/docs/dev/install.html)
#### Machine Learning
- [Lasagne](https://lasagne.readthedocs.io/)
- [Scikit-Learn](http://scikit-learn.org/stable/install.html)
- [Tensorflow](https://www.tensorflow.org/install/)
- [Theano](http://deeplearning.net/software/theano/)
#### Mathematical Computations
- [SciPy](https://www.scipy.org/install.html)
- [NumPy](http://www.numpy.org/)

### Android
Not listed.

### PHP
Not listed.

## Installation
The following instructions describe how to set up the project on a linux machine. The commands below were tested on Ubuntu 17.10 x64. However, the source code is cross-platform and can be set up on MacOS or Windows similarly, too. In some cases, you may need to use equivalent commands for your OS.

1. Clone source code on your local machine
    ```
    git clone https://github.com/bytexcite/versign
    ```

2. You must have Python 2.7.X installed on your machine. Check your Python version with `python -V`. If you do not have Python installed, please see installation [instructions](https://www.python.org/downloads/) for your platform. On Ubuntu, we were able to install it using:
    ```
    sudo apt-get install python
    ```

3. You will need Python's package manager `pip` to download rest of the dependencies. Make sure that you have it by typing `pip` in terminal and pressing Enter. If it gives an error, get it with:
    ```
    sudo apt-get install python-pip
    ```
    
Next, you need to install all of the dependencies of the project, as listed under Dependencies above. Skip any which you already have. To check if a certain package is installed, open Python console with `python` and then try importing that package using `import <package-name>`. It should give an `ImportError` if the package is not installed.

4. Some of these can be installed with `pip`. Run the following
    ```
    pip install Pillow
    pip install opencv-python
    pip install "Theano==0.9"
    pip install https://github.com/Lasagne/Lasagne/archive/master.zip
    pip install numpy
    pip install scipy
    pip install -U scikit-learn
    pip install scikit-image
    ```
5. Tkinter is required for handling GUI. If not already installed (it should be!), run the following on Ubuntu:
    ```
    sudo apt-get install python-tk
    ```

## PROBLEM STATEMENT
Forged signatures on bank cheques and legal documents, etc. leads to financial and legal fraud which can hinder justice or cause economic harm to individuals, organisations and/or states. We will address this problem in our semester project by designing a generic system which can be installed in different environments to combat fraud through signature forgery.

## OUR SOLUTION
Our solution is a client-server system designed to make offline signature verification accessible. Offline signature verification works on scanned images as opposed to online signature verification, which has access to dynamic signature data. Although considered more difficult than online verification, our solution focuses on offline verification because of its more practicability in real environments.

### Major Components
Our solution has the following five major components: A machine learning algorithm for verifying signatures offline in Python programming language, implemented as an independ, reusable library which can be used in any systems that may need it. A web application for registering individuals and providing their training data (i.e. signatures). A database for storing profiles of individuals and their samples of their signatures which the verification algorithm will use. Smartphone applications for capturing signatures and sending them to the web server for verification. Client application will display profile of the matching individual if the signature is verified. A web program for receiving scanned signatures from client applications, verifying the signature using training data in database and the Python library, and sending verification status and matching profile to the requesting client. For each environment where this system is installed, there would be a centralized database and a centralized web program for signature verification, and multiple client devices for scanning signatures. The web application will be accessible to system administrators through secure credentials, and the client applications for each installation environment will be connected to the centralized database of that particular installation environment.

### Languages and Tools
- Java/XML
- PHP
- MySQL
- Python
- HTML/CSS/JavaScript

## OUR SOLUTION’S NOVELTY
The novelty of our system comes from its generic design, which lends it to deployment in multiple, varying environments with little to no alteration. For example, it may be installed for use in banks, individual organizations, or even at state level. One scenario where our solution may be relevant is detailed below.
