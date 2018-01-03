#!/usr/bin/python
from Tkinter import *

# Create a new window
root = Tk()
root.title("VeriSign")                      # Set window title
root.geometry('{}x{}'.format(800, 600))     # Set window size (800px by 600px)
root.resizable(width=False, height=False)   # Make it fix-sized

def open_image():
    print "click!"

b = Button(master, text="OK", command=callback)
b.pack()

# TODO: Application logic goes here

# Enter main loop
root.mainloop()