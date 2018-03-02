# import the necessary packages
from abc import ABCMeta, abstractmethod
from PIL import Image
from PIL import ImageTk
from scipy import ndimage

import cv2
import numpy as np
import threading
import time
import tkFileDialog
import Tkinter as tk
 
from segment import extract_signature

#import mysql.connector

#cnx = mysql.connector.connect(user='root', password='root',
#                              host='localhost',
#                              database='versign')

#cursor = cnx.cursor()

#query = ("SELECT username, password FROM staff WHERE username = ''")
#cursor.execute(query)

#for (first_name, last_name, hire_date) in cursor:
#  print("{}, {} was hired on {:%d %b %Y}".format(
#    last_name, first_name, hire_date))

#cursor.close()
#cnx.close()

class Activity:
	__metaclass__ = ABCMeta

	@abstractmethod
	def display(self, app, args=None):
		pass

class SplashScreen(Activity):
	def display(self, app, args=None):
		background_image=ImageTk.PhotoImage(Image.open("../res/splash.png"))
		background_label = tk.Label(app.window, image=background_image, width=795, height=595)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		background_label.image = background_image
		background_label.grid(rowspan=3, columnspan=3, sticky="news")

		app.scheduleActivity(LoginScreen(), 1.0)

class LoginScreen(Activity):
	def display(self, app, args=None):
		def onLoginClicked():
			app.startActivity(MainMenu())

		background_image=ImageTk.PhotoImage(Image.open("../res/bg.png"))
		background_label = tk.Label(app.window, image=background_image, width=795, height=595)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		background_label.image = background_image
		background_label.grid(rowspan=3, columnspan=3, sticky="news")

		container = tk.Frame(app.window, bg="systemTransparent")
		container.grid(row=1, column=1)

		tk.Label(container, text="Username", fg="white", bg="systemTransparent", width="20", anchor="w").grid(row=1, column=1)
		tk.Label(container, text="Password", fg="white", bg="systemTransparent", width="20", anchor="w").grid(row=3, column=1, pady=("10", "1"))

		tk.Entry(container, width="20").grid(row=2, column=1)
		tk.Entry(container, show="*", width="20").grid(row=4, column=1)

		tk.Button(container, width="10", text="Login", command=onLoginClicked).grid(row=5, column=1, pady="30")

class MainMenu(Activity):
	def display(self, app, args=None):
		def onLogoutClicked():
			app.startActivity(LoginScreen())

		def onRegisterClicked():
			app.startActivity(RegistrationActivity())

		def onVerifyClicked():
			app.startActivity(VerificationActivity())

		background_image=ImageTk.PhotoImage(Image.open("../res/bg.png"))
		background_label = tk.Label(app.window, image=background_image, width=795, height=595)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		background_label.image = background_image
		background_label.grid(rowspan=3, columnspan=3, sticky="news")

		tk.Button(app.window, text="Sign Out", command=onLogoutClicked).grid(row=0, columnspan=3, sticky="ne", padx="25", pady="25")

		container = tk.Frame(app.window, bg="systemTransparent")
		container.grid(row=1, column=1)

		tk.Button(container, width="15", text="REGISTER", command=onRegisterClicked).grid(row=1, column=1, ipady="5")
		tk.Button(container, width="15", text="VERIFY", command=onVerifyClicked).grid(row=2, column=1, pady=("15", "0"), ipady="5")

class RegistrationActivity(Activity):
	def display(self, app, args=None):
		def onLogoutClicked():
			app.startActivity(MainMenu())

		background_image=ImageTk.PhotoImage(Image.open("../res/bg.png"))
		background_label = tk.Label(app.window, image=background_image, width=795, height=595)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		background_label.image = background_image
		background_label.grid(rowspan=6, columnspan=5, sticky="news")

		tk.Button(app.window, text="< Back", command=onLogoutClicked).grid(row=0, columnspan=5, sticky="nw", padx="25", pady="25")

		imageView =  tk.Label(app.window)
		imageView.configure(background="white")
		imageView.grid(row=1, column=1, columnspan=3, rowspan=3, ipadx="5", ipady="5", sticky="news")

		tk.Label(app.window, text="User ID", fg="white", bg="systemTransparent", width="20", anchor="e").grid(row=4, column=1)
		tk.Entry(app.window, show="*", width="20").grid(row=4, column=2)

		btn = tk.Button(app.window, text="Register")
		btn.grid(row=5, column=2, ipadx="10", ipady="10")

class VerificationActivity(Activity):
	def __init__(self):
		self.srcImgHolder = None
		self.destImgHolder = None

	def resize(self, source, canvas_size):
		src_w, src_h = source.size
		dest_w, dest_h = canvas_size
		if src_w == 0 or src_h == 0:
			output = Image.fromarray(np.ones(canvas_size).transpose() * 255.0)
		
		else:
			aspect_source = src_w / float(src_h)
			aspect_canvas = dest_w / float(dest_h)

			if aspect_source > aspect_canvas:
				new_w = int(dest_w)
				new_h = int(src_h * float(dest_w)/src_w)
			else:
				new_w = int(src_w * float(dest_h)/src_h)
				new_h = int(dest_h)

			output = source.resize((new_w, new_h), Image.ANTIALIAS)
	
		print "Source:", source.size, "Canvas:", canvas_size, "Output:", output.size
		return output

	def setSourceImage(self, sourceImage, window):
		sourceImage = ImageTk.PhotoImage(sourceImage)

		self.srcImgHolder.configure(image=sourceImage)
		self.srcImgHolder.image=sourceImage

	def setSignatureImage(self, signatureImage, window):
		signatureImage = ImageTk.PhotoImage(signatureImage)

		self.destImgHolder.configure(image=signatureImage)
		self.destImgHolder.image=signatureImage

	def display(self, app, args=None):
		def onLogoutClicked():
			app.startActivity(MainMenu())

		def openImage():
			# open a file chooser dialog and allow the user to select an input image
			path = tkFileDialog.askopenfilename()
	    
			# ensure a file path was selected
			if len(path) > 0:
				sourceImg = cv2.imread(path)
				sourceImg = cv2.cvtColor(sourceImg, cv2.COLOR_BGR2RGB)
				sourceImg = Image.fromarray(sourceImg)
				sourceImg = self.resize(sourceImg, (self.srcImgHolder.winfo_width(), self.srcImgHolder.winfo_height()))
				self.setSourceImage(sourceImg, app.window)

				# Extract signature and display when done
				signature = extract_signature(path, "../res/models/sgd.pkl")
				signature = Image.fromarray(signature).convert("RGB")
				signature = self.resize(signature, (self.destImgHolder.winfo_width(), self.destImgHolder.winfo_height()))
				self.setSignatureImage(signature, app.window)

		background_image=ImageTk.PhotoImage(Image.open("../res/bg.png"))
		background_label = tk.Label(app.window, image=background_image, width=795, height=595)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		background_label.image = background_image
		background_label.grid(rowspan=6, columnspan=6, sticky="news")

		tk.Button(app.window, text="Sign Out", command=onLogoutClicked).grid(row=0, columnspan=6, sticky="ne", padx="25", pady="25")

		self.srcImgHolder =  tk.Label(app.window)
		self.srcImgHolder.configure(background="white")
		self.srcImgHolder.grid(row=1, column=1, columnspan=3, rowspan=3, ipadx="5", ipady="5", sticky="news")

		self.destImgHolder =  tk.Label(app.window)
		self.destImgHolder.configure(background="white")
		self.destImgHolder.grid(row=1, column=4, columnspan=1, rowspan=3, ipadx="5", ipady="5", sticky="news")

		btn = tk.Button(app.window, text="Select Image", command=openImage)
		btn.grid(row=4, column=4, sticky="ne", pady="10")

		tk.Label(app.window, text="User ID", fg="white", bg="systemTransparent", width="20", anchor="e").grid(row=5, column=1)
		tk.Entry(app.window).grid(row=5, column=2, sticky="we")
		tk.Button(app.window, text="Verify").grid(row=5, column=3)

class App:
	def __init__(self, app_name="My Application", width=800, height=600, resizable=False):
		self.window = tk.Tk()
		self.window.configure(background="white")
		self.window.title=app_name
		self.window.resizable(width=resizable, height=resizable)
		self.window.geometry('{}x{}'.format(width, height))
		self.window.padx = "0"
		self.window.pady = "0"
		self.__centerOnScreen(self.window)

	def __centerOnScreen(self, window):
		window.update_idletasks()
		w = window.winfo_screenwidth()
		h = window.winfo_screenheight()
		size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
		x = w/2 - size[0]/2
		y = h/2 - size[1]/2 - 50
		window.geometry("%dx%d+%d+%d" % (size + (x, y)))

	def clear(self):
		for widget in self.window.winfo_children():
			widget.destroy()

	def scheduleActivity(self, activity, delay):
		def delayedTask():
			self.startActivity(activity)

		t = threading.Timer(delay, delayedTask)
		t.start() 

	def startActivity(self, activity, args=None):
		self.clear()
		activity.display(self, args)

	def startApp(self, firstActivity, args=None):
		self.startActivity(firstActivity, args)
		self.window.mainloop()

my_app = App("VeriSign v1.0")
my_app.startApp(SplashScreen())