# Offline Signature Verification

A complete system to detect frauds using forged signatures.

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
