import sys
rootDir = "../../versign-core/"
sys.path.append(rootDir)

from abc import ABCMeta, abstractmethod
from PIL import Image, ImageTk
from scipy import ndimage
from segment import extract_signature, find_signatures
from user_manager import register, is_registered
from verification import verify_signature

import cv2
import numpy as np
import threading
import time
import tkFileDialog
import Tkinter as tk
import tkMessageBox


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
	def __init__(self):
		self.destImgHolder = None
		self.userId = tk.StringVar()
		self.signatures = None

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

	def setSignatureImage(self, signatureImage, window):
		signatureImage = ImageTk.PhotoImage(signatureImage)

		self.destImgHolder.configure(image=signatureImage)
		self.destImgHolder.image=signatureImage

	def highlightLocatedSignatures(self, image, bounds):
		img = np.array(image)
		for bound in bounds:
			x, y, w, h = bound
			cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 3)

		return Image.fromarray(img)

	def display(self, app, args=None):
		def onLogoutClicked():
			app.startActivity(MainMenu())

		def onRegisterClicked():
			if self.userId.get() is "":
				tkMessageBox.showerror("Error", "User ID not provided")
				return

			if self.signatures is None:
				tkMessageBox.showerror("Error", "Reference signatures not provided")
				return
				
			userId = self.userId.get()
			if userId is not "" and self.signatures is not None:	
				if is_registered(userId, dirCore=rootDir):
					tkMessageBox.showerror(self.userId.get() + " already exists", "This user ID is already taken. Please provide a unique ID.")
					return
					
				refSigns = self.signatures
				#h, w = refSigns.shape
				#x = int(0.025*w)
				#y = int(0.025*h)
				#w = w - 2*x
				#h = h - 2*y
				#refSigns = refSigns[y:y+h, x:x+w]
				
				h, w = refSigns.shape

				if register(userId, refSigns, dirCore=rootDir):
					tkMessageBox.showinfo("Enrollment Result", "Enrollment successful")

		def openImage():
			# open a file chooser dialog and allow the user to select an input image
			path = tkFileDialog.askopenfilename()
	    
			# ensure a file path was selected
			if len(path) > 0:
				try:
					self.signatures = cv2.imread(path, 0)

					bounds = find_signatures(self.signatures)
					signature = Image.fromarray(cv2.imread(path)).convert("RGB")
					signature = self.highlightLocatedSignatures(signature, bounds)
					signature = self.resize(signature, (self.destImgHolder.winfo_width(), self.destImgHolder.winfo_height()))
					self.setSignatureImage(signature, app.window)
				except:
					tkMessageBox.showerror("Error", "No signature detected")

		background_image=ImageTk.PhotoImage(Image.open("../res/bg.png"))
		background_label = tk.Label(app.window, image=background_image, width=795, height=595)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		background_label.image = background_image
		background_label.grid(rowspan=60, columnspan=80, sticky="news")

		rootView = app.window #tk.Frame(app.window)
		#rootView.grid(rowspan=60, columnspan=80, ipadx="10", ipady="10", sticky="news")

		self.backButtonImage=ImageTk.PhotoImage(Image.open("../res/ic_button_back.png"))
		backButton = tk.Button(rootView, command=onLogoutClicked)
		backButton.config(image=self.backButtonImage)
		backButton.grid(row=1, column=1, padx="5", pady="5")

		instructions_image=ImageTk.PhotoImage(Image.open("../res/instructions.png"))
		instructionsView = tk.Label(rootView, image=instructions_image, width=275, height=400)
		instructionsView.configure(background="black")
		instructionsView.place(x=0, y=0, relwidth=1, relheight=1)
		instructionsView.image = instructions_image
		instructionsView.grid(row=2, column=2, rowspan=55, columnspan=30, sticky="news")

		self.captureButtonImage=ImageTk.PhotoImage(Image.open("../res/btn_capture.png"))
		captureButton = tk.Button(rootView, command=openImage)
		captureButton.config(image=self.captureButtonImage, width="80", height="25")
		captureButton.grid(row=35, column=16, sticky="ew", padx="10")

		userIdField = tk.Entry(rootView, textvariable=self.userId)
		userIdField.grid(row=45, column=12, columnspan=15, sticky="ew")

		self.registerButtonImage=ImageTk.PhotoImage(Image.open("../res/btn_register.png"))
		registerButton = tk.Button(rootView, command=onRegisterClicked)
		registerButton.config(image=self.registerButtonImage, width="80", height="25")
		registerButton.grid(row=55, column=16, sticky="ew", padx="10")

		self.destImgHolder =  tk.Label(rootView, borderwidth=2, relief="solid")
		self.destImgHolder.configure(background="white")
		self.destImgHolder.grid(row=2, column=33, rowspan=55, columnspan=40, ipadx="5", ipady="5", sticky="news")

class VerificationActivity(Activity):
	def __init__(self):
		self.destImgHolder = None
		self.userId = tk.StringVar()
		self.signature = None

		self.v = tk.IntVar()
		self.v.set(1)

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

	def setSignatureImage(self, signatureImage, window):
		signatureImage = ImageTk.PhotoImage(signatureImage)

		self.destImgHolder.configure(image=signatureImage)
		self.destImgHolder.image=signatureImage

	def display(self, app, args=None):
		def onLogoutClicked():
			app.startActivity(MainMenu())

		def onVerifyClicked():
			if self.userId.get() is "":
				tkMessageBox.showerror("Error", "User ID not provided")
				return

			if self.signature is None:
				tkMessageBox.showerror("Error", "Signature not provided")
				return
				
			userId = self.userId.get()
			if userId is not "" and self.signature is not None:	
				if not is_registered(userId, dirCore=rootDir):
					tkMessageBox.showerror(self.userId.get() + " not found", "No such user exists. Add a new user using the Register menu.")
					return
				
				result = verify_signature(userId, self.signature, rootDir)
				self.signature = None
				if result is True:
					tkMessageBox.showinfo("Verification Result", "GENUINE. Signature belongs to user '" + self.userId.get() + "'")
				else:
					tkMessageBox.showinfo("Verification Result", "FORGED. Signature does not belong to user '" + self.userId.get() + "'")

		def openImage():
			# open a file chooser dialog and allow the user to select an input image
			path = tkFileDialog.askopenfilename()
	    
			# ensure a file path was selected
			if len(path) > 0:
				try:
					if self.v.get() == 1:
						self.signature = extract_signature(cv2.imread(path, 0), rootDir + "/db/models/tree.pkl")
					else:
						self.signature = cv2.imread(path, 0)
					
					w, h = self.signature.shape
					if w is 0 or h is 0:
						raise exception()

					signature = Image.fromarray(self.signature).convert("RGB")
					signature = self.resize(signature, (self.destImgHolder.winfo_width(), self.destImgHolder.winfo_height()))
					self.setSignatureImage(signature, app.window)
				except:		
					tkMessageBox.showerror("Error", "No signature detected")
		background_image=ImageTk.PhotoImage(Image.open("../res/bg.png"))
		background_label = tk.Label(app.window, image=background_image, width=795, height=595)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		background_label.image = background_image
		background_label.grid(rowspan=6, columnspan=6, sticky="news")

		tk.Button(app.window, text="< Back", command=onLogoutClicked).grid(row=0, columnspan=6, sticky="nw", ipadx="5", ipady="2", padx="25", pady="25")

		containerLt=tk.Frame(app.window, borderwidth=2, relief="solid")
		containerLt.grid(row=1, column=1, rowspan=3, columnspan=1, ipadx="5", ipady="5", sticky="news")

		tk.Label(containerLt, text="INPUT TYPE", font='Helvetica 14 bold').grid(row=0, sticky="nw")
		tk.Radiobutton(containerLt, text="Cheque", variable=self.v, value=1).grid(row=1, sticky="nw")
		tk.Radiobutton(containerLt, text="Signature", variable=self.v, value=2).grid(row=2, sticky="nw")
		tk.Radiobutton(containerLt, text="Document", variable=self.v, value=3).grid(row=3, sticky="nw")
		
		tk.Label(containerLt, text="ENTER USER ID", font='Helvetica 14 bold').grid(row=4, stick="nw", pady=("10", "0"))
		tk.Entry(containerLt, textvariable=self.userId).grid(row=5, column=0, sticky="ew")

		self.destImgHolder = tk.Label(app.window, borderwidth=2, relief="solid")
		self.destImgHolder.configure(background="white")
		self.destImgHolder.grid(row=1, column=2, rowspan=3, columnspan=3, ipadx="5", ipady="5", sticky="news")

		tk.Button(app.window, text="  1) OBTAIN SIGNATURE  ", command=openImage, borderwidth=2, relief="solid", anchor='w').grid(row=4, column=4, sticky="w", padx="10")
		tk.Button(app.window, text="  2) VERIFY SIGNATURE  ", command=onVerifyClicked, borderwidth=2, relief="solid", anchor='w').grid(row=5, column=4, sticky="nw", padx="10")

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
my_app.startApp(RegistrationActivity())