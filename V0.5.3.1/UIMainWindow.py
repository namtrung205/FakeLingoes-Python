# -*- coding: utf-8 -*-
# UI Main
from PyQt5.QtCore import QFile, QIODevice, Qt, QTextStream, QEvent, QSize,QPoint

from PyQt5.QtGui import QIcon, QShortcutEvent, QKeySequence, QFont, QPixmap
from PyQt5.QtWidgets import (QDialog, QFileDialog, QGridLayout, QHBoxLayout, QMessageBox,
		QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QComboBox, QRadioButton, QCheckBox,
		QWidget, QShortcut, QApplication,QSystemTrayIcon,QStyle,QAction,qApp, QMenu, QDesktopWidget, QTabWidget, QDoubleSpinBox)

# Local
from MeaningWindow import *
from customeWidgets import *
from myStranslator import *
from V3WindowSelection import *
from V3Image2Text import *

from Speak import *
# from ImportToDatabase import *

#  Pip pypi
from gtts import gTTS
from gtts.tts import gTTSError
import playsound

# Bulld-in
import os
import time
from multiprocessing import Pool, TimeoutError
import re
# pyWin32
import ctypes
from win32api import GetMonitorInfo, MonitorFromPoint
from win32gui import SetWindowPos
import win32con

# Incon
# myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string

# Win7 no comment bellow line
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from myTimers import myTimer


# Monitor
monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
work_area = monitor_info.get("Work")
heightMonitor = work_area[3]
widthMonitor = work_area[2]

# Support language
myLangDict = {
				'English':'en',
				'Vietnamese':'vi',
			 }

# listNameLang = sorted(list(myLangDict.keys()))

# E:\DEV\02. Fake lingoes and ocr\V5.4\Resources\Dictionaries\English_Vietnamese_Dic.txt
# Impoert tu dien vao trong 
lingoesDic = {}

# Open file
LingoesDicTxt = open(".\Resources\Dictionaries\English_Vietnamese_Dic.txt", 'r', encoding="utf-8")

for line in LingoesDicTxt:
	listWordLine = list(str(line).split("|"))
	lingoesDic[str(listWordLine[1])] = listWordLine[2]

myLingoesListWords = lingoesDic.keys()

lingoesModel = QtCore.QStringListModel()
lingoesModel.setStringList(myLingoesListWords)

lingoesCompleter = QtWidgets.QCompleter()
lingoesCompleter.setModel(lingoesModel)




class TranslateMainWindow(QWidget):
	"""docstring for TranslateTool"""

	# API:
	SpaceOCR_apiKey = None

	Oxford_appID = None
	Oxford_appKey = None

	# Limit time out:
	myTimeOutTrans = 8
	myTimeOutCap = 12

	timeStart = 0.00
	timeFinished = 0.00

	## Font UI
	# Input Font
	inputFont = QFont()
	inputFont.setPointSize(12)
	inputFont10 = QFont()
	inputFont10.setPointSize(10)

	# lable Font
	lableFont = QFont()
	lableFont.setPointSize(10)

	# out Font
	outputFont1 = QFont()
	outputFont1.setPointSize(9)

	outputFont2 = QFont()
	outputFont2.setPointSize(13)
	

	outputFont3 = QFont()
	outputFont3.setPointSize(9)

	# Constructor
	def __init__(self, parent = None):
		super(TranslateMainWindow, self).__init__(parent)


		### WINDOW Start Setting
		#Window (title, Icon, size...):
		self.setWindowTitle("Fake Lingoes-UI")
		# self.setMouseTracking(True)
		self.setWindowIcon(QIcon("icon.ico"))		
		self.setWindowOpacity(0.9)
		self.setFixedSize(400,150)
		self.center()
		self.oldPos = self.pos()

		# Window flag
		self.setWindowFlags(
		Qt.Window |
		Qt.CustomizeWindowHint |
		Qt.WindowStaysOnTopHint |
		Qt.Tool|
		Qt.FramelessWindowHint
		)

		# Properties non UI
		# Clipboard
		self.clipboard = QApplication.clipboard()
		self.clipboard.dataChanged.connect(self.detectClipboardUrl)
		self.clipboard
		
		# Temp files, Folders, variable...
		self.myPathMp3 = ".\\Tempfile\\myTts.mp3"
		self.fileCount = 0

		self.fromSym = "en"
		self.toSym = 'vi'


		##System Tray Icon
		self.trayIcon = QIcon(QPixmap('icon.ico'))
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.showMessage("QString title", "QString msg",QSystemTrayIcon.Information,2000)
		self.tray_icon.setIcon(self.trayIcon)
		self.tray_icon.activated.connect(self.icon_clicked)

		self.show_action = QAction("Stay On Top", self)
		self.show_action.setCheckable(True)
		self.show_action.setChecked(True)
		self.show_action.triggered.connect(self.alwayTop_enable)

		hide_action = QAction("Hide", self)
		hide_action.triggered.connect(self.hideButton_Clicked)

		self.trans_clipboard_action = QAction("Translate Clipboard Text", self)
		self.trans_clipboard_action.setCheckable(True)
		self.trans_clipboard_action.setChecked(True)

		quit_action = QAction("Exit", self)
		quit_action.triggered.connect(qApp.quit)
		tray_menu = QMenu()
		tray_menu.addAction(self.trans_clipboard_action)
		tray_menu.addSeparator()
		tray_menu.addAction(self.show_action)
		tray_menu.addAction(hide_action)
		tray_menu.addAction(quit_action)
		self.tray_icon.setContextMenu(tray_menu)
		self.tray_icon.show()

		self.myMenu = QMenu()
		self.myMenu.addAction(self.show_action)
		self.myMenu.addAction(hide_action)
		self.myMenu.addAction(quit_action)
		self.myMenu.addAction(self.trans_clipboard_action)

		# Shortcut
		
		self.transShortcut = QShortcut(QKeySequence("Alt+D"),self)
		self.transShortcut.activated.connect(self.transButton_Click)

		self.transEnterShortcut = QShortcut(QKeySequence("return"),self)
		self.transEnterShortcut.activated.connect(self.transButton_Click)

		self.righSnapShortcut = QShortcut(QKeySequence("Ctrl+F"),self)
		self.righSnapShortcut.activated.connect(self.largeButton_Click)

		self.hideShortcut = QShortcut(QKeySequence("Alt+H"),self)
		self.hideShortcut.activated.connect(self.hideButton_Clicked)

		self.swapShortcut = QShortcut(QKeySequence("Alt+X"),self)
		self.swapShortcut.activated.connect(self.swapButton_Clicked)

		self.capImage_ApiShortcut = QShortcut(QKeySequence("Alt+I"),self)
		self.capImage_ApiShortcut.activated.connect(self.captureApiButton_click)

		self.capImageShortcut = QShortcut(QKeySequence("Alt+W"),self)
		self.capImageShortcut.activated.connect(self.captureAreaButton_click)

		## Main UI and Widgets
		# Top bar (row 1)

		self.captureAreaButton = myIconButton()
		selectAreaIcon = QIcon()
		selectAreaIcon.addPixmap(QPixmap(".\\Resources\\Images\\SelectArea.png"))
		self.captureAreaButton.setFlat(True)
		self.captureAreaButton.setIcon(selectAreaIcon)
		self.captureAreaButton.setIconSize(QSize(16,16))
		self.captureAreaButton.setFixedSize(16, 16)
		self.captureAreaButton.setToolTip('Translate Image')


		self.captureApiButton = myIconButton()
		selectAreaApiIcon = QIcon()
		selectAreaApiIcon.addPixmap(QPixmap(".\\Resources\\Images\\claroreadcloud.png"))
		self.captureApiButton.setFlat(True)
		self.captureApiButton.setIcon(selectAreaApiIcon)
		self.captureApiButton.setIconSize(QSize(20,20))
		self.captureApiButton.setFixedSize(20, 20)
		self.captureApiButton.setToolTip('Translate Image Online')


		# # Button hide
		# self.hideButton = myIconButton()
		# iconhide = QIcon()
		# iconhide.addPixmap(QPixmap(".\\images\\hide.png"))
		# self.hideButton.setFlat(True)
		# self.hideButton.setIcon(iconhide)
		# self.hideButton.setIconSize(QSize(20,20))
		# self.hideButton.setFixedSize(20,20)
		# self.hideButton.setToolTip("Hide into System Tray")


		# input text Line Raw
		self.inputBoxRaw = QLineEdit()
		self.inputBoxRaw.setPlaceholderText("Tu (cum tu) can dich...")
		self.inputBoxRaw.setFont(self.inputFont)
		self.inputBoxRaw.setCompleter(lingoesCompleter)

		# input text Line
		self.inputBox = QTextEdit()
		self.inputBox.hide()
		# self.inputBox.setTextCursor()
		# self.inputBox.setReadOnly(True)

		self.inputBox.setMaximumHeight(300)
		self.inputBox.setPlaceholderText("Tu (cum tu) can dich...")
		self.inputBox.setFont(self.inputFont10)


		self.transButton = myIconButton()
		iconTrans = QIcon()
		iconTrans.addPixmap(QPixmap(".\\Resources\\Images\\trans.png"))
		self.transButton.setFlat(True)
		self.transButton.setIcon(iconTrans)
		self.transButton.setIconSize(QSize(20,20))
		self.transButton.setFixedSize(20, 20)
		self.transButton.setToolTip('Translate')




		# Button Listen Mode
		self.streamButton = myIconButton()
		self.iconStreamG = QIcon()
		self.iconStreamG.addPixmap(QPixmap(".\\Resources\\Images\\StreamMusicG.png"))
		self.streamButton.setFlat(True)
		self.streamMode = "G"
		
		self.iconStreamM = QIcon()
		self.iconStreamM.addPixmap(QPixmap(".\\Resources\\Images\\StreamMusicM.png"))
		self.streamButton.setFlat(True)

		self.streamButton.setIcon(self.iconStreamG)
		self.streamButton.setIconSize(QSize(20,20))
		self.streamButton.setFixedSize(20, 20)
		self.streamButton.setToolTip('Google listen')


		# Button Listen
		self.listenButton = myIconButton()
		iconListen = QIcon()
		iconListen.addPixmap(QPixmap(".\\Resources\\Images\\Listen.png"))
		self.listenButton.setFlat(True)
		self.listenButton.setIcon(iconListen)
		self.listenButton.setIconSize(QSize(20,20))
		self.listenButton.setFixedSize(20,20)
		self.listenButton.setToolTip("Listen")


		# Rate SpinBox
		self.rateSpin = QDoubleSpinBox()
		self.rateSpin.setRange(0.5, 2)
		self.rateSpin.setSingleStep(0.25)
		self.rateSpin.setValue(1.00)
		self.rateSpin.setToolTip("Change speak rate.")


		# Button large
		self.largeButton = myIconButton()
		iconLarge = QIcon()
		iconLarge.addPixmap(QPixmap(".\\Resources\\Images\\large.png"))
		self.largeButton.setFlat(True)
		self.largeButton.setIcon(iconLarge)
		self.largeButton.setIconSize(QSize(20,20))
		self.largeButton.setFixedSize(20,20)
		self.largeButton.setToolTip("Change Viewsize")


		# Row 2
		self.outputBox = myTextEdit()
		self.outputBox.setFont(self.outputFont2)

		# row 3
		# input lable
		self.inputLabel = QLabel("English")
		self.inputLabel.setFont(self.lableFont)

		self.swapButton = myIconButton()
		iconSwap = QIcon()
		iconSwap.addPixmap(QPixmap(".\\Resources\\Images\\swap.png"))
		self.swapButton.setFlat(True)
		self.swapButton.setIcon(iconSwap)
		self.swapButton.setIconSize(QSize(20,20))
		self.swapButton.setFixedSize(20,20)
		self.swapButton.setToolTip("Swap Language")

		# out lable
		self.outputLabel = QLabel("Vietnamese")
		self.outputLabel.setFont(self.lableFont)


		# status lable
		self.isRunning = False

		self.statusLabel = QLabel("No Notification.")
		# self.statusLabel.setStyleSheet("QLabel{color: rgb(26, 0, 0);}")
		self.statusLabel.setFont(self.lableFont)
		self.statusLabel.setFixedWidth(100)		

		self.expandButton = myIconButton()
		iconExpand = QIcon()
		iconExpand.addPixmap(QPixmap(".\\Resources\\Images\\expand.png"))
		self.expandButton.setFlat(True)
		self.expandButton.setIcon(iconExpand)
		self.expandButton.setIconSize(QSize(16,16))
		self.expandButton.setFixedHeight(20)
		self.expandButton.setToolTip("Expand")

		## LAYOUT
		# topbar
		topBarLayout = QHBoxLayout()
		topBarLayout.addSpacing(5)
		topBarLayout.addWidget(self.captureAreaButton)
		topBarLayout.addWidget(self.captureApiButton)
		# topBarLayout.addWidget(self.hideButton)
		topBarLayout.addWidget(self.inputBoxRaw)
		topBarLayout.addWidget(self.transButton)
		topBarLayout.addWidget(self.streamButton)
		topBarLayout.addWidget(self.listenButton)
		topBarLayout.addWidget(self.rateSpin)
		topBarLayout.addWidget(self.largeButton)
		topBarLayout.addSpacing(5)

		# Midbar
		midBarLayout = QHBoxLayout()
		midBarLayout.addSpacing(5)
		midBarLayout.addWidget(self.inputLabel)
		midBarLayout.addWidget(self.swapButton)
		midBarLayout.addWidget(self.outputLabel)
		midBarLayout.addStretch()
		midBarLayout.addWidget(self.statusLabel)
		midBarLayout.addSpacing(15)
		midBarLayout.addWidget(self.expandButton)

		# Main layout
		mainLayout = QVBoxLayout()
		mainLayout.setContentsMargins(1,1,2,1)
		mainLayout.addSpacing(2)
		# mainLayout.addLayout(ImageBarLayout)
		mainLayout.addLayout(topBarLayout)
		mainLayout.addWidget(self.inputBox)
		mainLayout.addSpacing(-3)
		mainLayout.addWidget(self.outputBox)
		mainLayout.addSpacing(-3)
		mainLayout.addLayout(midBarLayout)
		mainLayout.addSpacing(-2)


		self.meaningdWindow = MeaningWindow(self.Oxford_appID, self.Oxford_appKey, self.inputBox.toPlainText())
		self.meaningdWindow.move(self.x(), self.y()+150)

		self.setLayout(mainLayout)

		##CONNECT AND OTHER EVENT
		# top bar
		# Capture
		self.captureAreaButton.clicked.connect(self.captureAreaButton_click)
		self.captureApiButton.clicked.connect(self.captureApiButton_click)

		# Input box
		self.inputBoxRaw.textChanged.connect(self.inputRaw_changed)
		self.inputBox.textChanged.connect(self.input_changed)

		# function trans and listen
		# self.hideButton.clicked.connect(self.hideButton_Clicked)
		self.transButton.clicked.connect(self.transButton_Click)
		self.streamButton.clicked.connect(self.streamButton_Click)
		self.listenButton.clicked.connect(self.listenButton_Click)
		self.largeButton.clicked.connect(self.largeButton_Click)


		# mid bar
		self.swapButton.clicked.connect(self.swapButton_Clicked)
		self.expandButton.clicked.connect(self.expandButton_Click)

		# self.meaningdWindow.addToDbButton.clicked.connect(self.addToDbButton_Click)


		# Capture
		self.wincap = CaptureWindow()
		self.wincap.hide()
	
	# Group1: Function when start and reaction wiht mainwindow
	# Start
	# Drag Move lessFrame
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()
		# print("Press: " + str(event.x()) + ", " +str(event.y()))

	def mouseMoveEvent(self, event):
		delta = QPoint (event.globalPos() - self.oldPos)
		#print(delta)
		self.move(self.x() + delta.x(), self.y() + delta.y())

		if self.height() <200:
			self.meaningdWindow.move(self.x() + delta.x(), self.y() + delta.y()+self.height())
		else:
			self.meaningdWindow.move(self.x() - self.meaningdWindow.width() + delta.x(), self.y() + delta.y())

		self.oldPos = event.globalPos()


	# System tray menu functions
	def alwayTop_enable(self):
		if not self.show_action.isChecked():
			self.setWindowFlags(
			Qt.Window |
			Qt.CustomizeWindowHint |
			Qt.Tool|
			Qt.FramelessWindowHint
			)

			self.meaningdWindow.setWindowFlags(self.windowFlags())

			self.move(widthMonitor - self.width(), 40)			
			self.show()
		else:
			self.setWindowFlags(
			Qt.Window |
			Qt.CustomizeWindowHint |
			Qt.WindowStaysOnTopHint |
			Qt.Tool|
			Qt.FramelessWindowHint
			)
			self.meaningdWindow.setWindowFlags(self.windowFlags())

			self.move(widthMonitor - self.width(), 40)
			self.show()

	def show2(self):
		self.meaningdWindow.hide()

		SetWindowPos(self.winId(),
             win32con.HWND_TOPMOST, # = always on top. only reliable way to bring it to the front on windows
             0, 0, 0, 0,
             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
		SetWindowPos(self.winId(),
             win32con.HWND_NOTOPMOST, # disable the always on top, but leave window at its top position
             0, 0, 0, 0,
             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
		
		self.raise_()
		self.show()
		self.activateWindow()


	### Group2: Topbar
	# capture function


	def icon_clicked(self, reason):
		if reason == QSystemTrayIcon.Trigger:
			if not self.isHidden():
				self.hide()
				self.meaningdWindow.hide()
			else:
				self.show2()
		else:
			pass

	def showOrHide(self):
		if not self.isHidden():
			self.hide()
			self.meaningdWindow.hide()
		else:
			self.show2()




	def captureApiButton_click(self):
		try:
			self.functionStart()

			self.hideButton_Clicked()
			self.wincap.close()
			self.wincap = CaptureWindow()
			# self.wincap.update()
			self.wincap.show()
			self.wincap.capButton.clicked.connect(self.WinCap_CapButton_Api_Click)
			self.wincap.capShortcut.activated.connect(self.WinCap_CapButton_Api_Click)
			self.wincap.cancelShortcut.activated.connect(self.cancel_Capture_active)
		except Exception as e:
			QMessageBox.information(self, "Information", "Error Wincap " + str(e))
		self.functionFinished()

 	# non limit time

	# def WinCap_CapButton_Api_Click(self):
	# 	startTime = time.time()
	# 	self.functionStart()

	# 	self.wincap.Area = (min(self.wincap.p1.x(),self.wincap.p2.x()) ,min(self.wincap.p1.y(),self.wincap.p2.y()) ,max(self.wincap.p1.x(),self.wincap.p2.x()), max(self.wincap.p1.y(),self.wincap.p2.y()))
	# 	# print(self.wincap.a)
	# 	self.wincap.hide()
	# 	time.sleep(0.5)
	# 	self.wincap.capture(self.wincap.Area)

	# 	self.show()

	# 	# textFromImageApi = myTimer(ImageToText_Api, (".\Capture\\capture.png"), 10)

	# 	self.inputBox.setText(ImageToText_Api())
	# 	self.transButton_Click()

	# 	print("cap_Api: Take" + str(startTime - time.time()))


	# Limit time
	def WinCap_CapButton_Api_Click(self):
		try:
			self.functionStart()

			self.wincap.Area = (min(self.wincap.p1.x(),self.wincap.p2.x()) ,min(self.wincap.p1.y(),self.wincap.p2.y()) ,max(self.wincap.p1.x(),self.wincap.p2.x()), max(self.wincap.p1.y(),self.wincap.p2.y()))
			# print(self.wincap.a)
			if self.wincap.Area[0] == self.wincap.Area[2] or self.wincap.Area[1] == self.wincap.Area[3]:
				QMessageBox.information(self, "Information", "window area too small, select again or press 'ECS' to cancel!")
				print("window area too small")
				self.captureApiButton_click()
			else:
				self.wincap.hide()
				time.sleep(0.5)
				self.wincap.capture(self.wincap.Area)

				self.show()

				textFromImageApi = myTimer(ImageToText_Api, (self.SpaceOCR_apiKey, ".\Capture\\capture.png",), self.myTimeOutCap)

				self.inputBox.setText(textFromImageApi)
				self.transButton_Click()
		except Exception as e:
			QMessageBox.information(self, "Information", "Error Wincap " + str(e))			
		self.functionFinished()



	def captureAreaButton_click(self):
		try:
			self.functionStart()
			self.hideButton_Clicked()
			self.wincap.close()
			self.wincap = CaptureWindow()
			# self.wincap.update()
			self.wincap.show()
			self.wincap.capButton.clicked.connect(self.WinCap_CapButton_Click)
			self.wincap.capShortcut.activated.connect(self.WinCap_CapButton_Click)
			self.wincap.cancelShortcut.activated.connect(self.cancel_Capture_active)
		except NameError as e:
			QMessageBox.information(self, "Information", "Error Cap" + str(e))
		self.functionFinished()


	def WinCap_CapButton_Click(self):
		try:
			self.functionStart()

			self.wincap.Area = (min(self.wincap.p1.x(),self.wincap.p2.x()) ,min(self.wincap.p1.y(),self.wincap.p2.y()) ,max(self.wincap.p1.x(),self.wincap.p2.x()), max(self.wincap.p1.y(),self.wincap.p2.y()))
			print(self.wincap.Area)
			if self.wincap.Area[0] == self.wincap.Area[2] or self.wincap.Area[1] == self.wincap.Area[3]:
				QMessageBox.information(self, "Information", "window area too small, select again or press 'ECS' to cancel!")
				print("window area too small")
				self.captureAreaButton_click()
			else:
				self.wincap.hide()
				time.sleep(0.5)
				self.wincap.capture(self.wincap.Area)

				self.show()
				self.inputBox.setText(ImageToText())
				self.transButton_Click()
		except Exception as e:
			QMessageBox.information(self, "Information", "Error Wincap " + str(e))			
		self.functionFinished()


	def cancel_Capture_active(self):
		self.wincap.hide()
		# self.show()

	# Input function
	def inputRaw_changed(self):
		if not self.inputBoxRaw.isHidden():
			self.inputBox.setText(self.inputBoxRaw.text())
			
			print("from Raw --> Edit")
		else:
			print("Raw is hide")

	def input_changed(self):

		self.inputBoxRaw.setText(self.inputBox.toPlainText())
		self.meaningdWindow.inputWord = self.inputBox.toPlainText()
		self.meaningdWindow.Oxford_appID = self.Oxford_appID
		self.meaningdWindow.Oxford_appKey= self.Oxford_appKey
		print("text changed")
		self.autoChangeOut()

	def detectClipboardUrl(self):
		try:
			if not (self.trans_clipboard_action.isChecked()) :
				print("Auto trans clipboard off")
			else:
				# if self.isHidden():
				# 	self.show()
				print("clipboard change")
				print(self.clipboard.text())
				self.inputBox.setText(self.clipboard.text())

				# self.activateWindow()
				self.transButton_Click()
		except Exception as e:
			QMessageBox.information(self, "Information", str(e))			


	# Translate functions

	# def transButton_Click(self, text = ""):
	# 	self.functionStart()
	# 	timestart = time.time()
	# 	try:
	# 		if not self.show_action.isChecked():
	# 			self.show2()
	# 		self.meaningdWindow = MeaningWindow(self.inputBox.toPlainText())
	# 		self.meaningdWindow.move(self.x(), self.y()+150)
			
	# 		if text == "" or text == False:
	# 			mytext = self.inputBox.toPlainText()
	# 		self.outputBox.setPlainText(googleTrans(mytext, self.fromSym, self.toSym))
	# 		self.meaningdWindow.hide()
	# 		self.functionFinished()

	# 	except Exception as e:
	# 		QMessageBox.information(self, "Information", str(e) + "Error 2")
	# 		self.functionNotSuccess()
	# 	print("None check: " + str(time.time() - timestart))


	# #  Transwith limit time
	def transButton_Click(self, text = ""):
		self.functionStart()
		timestart = time.time()
		try:
			if not self.show_action.isChecked():
				self.show2()
			# self.meaningdWindow = MeaningWindow(self.Oxford_appID, self.Oxford_appKey,self.inputBox.toPlainText())
			self.meaningdWindow.move(self.x(), self.y()+150)
			
			if text == "" or text == False:
				mytext = str(self.inputBox.toPlainText()).lower()

				mytext2 = re.sub("^\s+|\s+$", "", mytext, flags=re.UNICODE)
			
			if mytext2 in myLingoesListWords:
				self.outputBox.setHtml(lingoesDic[mytext2])
				self.outputBox.setFont(self.outputFont3)
				
				if self.height() < 200:
					self.setFixedHeight(200)

			else:
				outText = myTimer(googleTrans,(mytext, self.fromSym, self.toSym), self.myTimeOutTrans )
				self.outputBox.setFont(self.outputFont3)
				outText = str(outText).replace("\n","<br>")
				outTextHtml = "<h3>%s<h3>" %outText

				if self.height() == 300:
					self.setFixedHeight(150)
				# self.outputBox.setPlainText(outText)
				self.outputBox.setHtml(outTextHtml)

			self.meaningdWindow.hide()
			self.functionFinished()

		except Exception as e:
			QMessageBox.information(self, "Information", str(e) + "Error 2")
			self.functionNotSuccess()
		print("None check: " + str(time.time() - timestart))


	# #  Transwith limit time
	def autoChangeOut(self, text = ""):
		self.functionStart()
		timestart = time.time()
		try:
			if not self.show_action.isChecked():
				self.show2()
			# self.meaningdWindow = MeaningWindow(self.Oxford_appID, self.Oxford_appKey,self.inputBox.toPlainText())
			self.meaningdWindow.move(self.x(), self.y()+150)
			
			if text == "" or text == False:
				mytext = str(self.inputBox.toPlainText()).lower()
				# " ".join(mytext.split())
				mytext = re.sub("^\s+|\s+$", "", mytext, flags=re.UNICODE)
			
			if mytext in myLingoesListWords:
				self.outputBox.setHtml(lingoesDic[mytext])
				self.outputBox.setFont(self.outputFont3)
				
				if self.height() < 200:
					self.setFixedHeight(200)
			else:
				self.outputBox.setHtml("<h3></h3>")

			self.meaningdWindow.hide()
			self.functionFinished()

		except Exception as e:
			QMessageBox.information(self, "Information", str(e) + "Error 2")
			self.functionNotSuccess()
		print("None check: " + str(time.time() - timestart))



	# Listen functions
	def streamButton_Click(self):
		if self.streamMode=="G":
			self.streamButton.setIcon(self.iconStreamM)
			self.streamMode="M"
		else:
			self.streamButton.setIcon(self.iconStreamG)
			self.streamMode="G"


	def outTextChange(self, saveName):
		tts = gTTS(self.inputBox.toPlainText())
		tts.lang = self.fromSym
		tts.save(saveName)


	def listenButtonG_Click(self):
		# start_time = time.time()
		self.functionStart()
		try:
			# self.transButton_Click()
			self.myPathMp3 = ".\\Tempfile\\myTts.mp3"
			self.outTextChange(self.myPathMp3)
			
		except (AssertionError, AttributeError, gTTSError):
			try:
				print("Gtts not available, use myPyttsx3")
				# QMessageBox.information(self, "Information", "Tạm thời không khả dụng.")
				if str(self.inputBox.toPlainText()).count(".") > 2 or str(self.inputBox.toPlainText()).count(" ") > 30:
					QMessageBox.information(self, "information", "Text is too long")
					return None
				else:
					myPyttsx3(self.inputBox.toPlainText(), int(self.rateSpin.value()*100))
					return None

			except :
				print("Error 10")
				return None

		except (NameError, PermissionError):
			try:
				self.fileCount+=1
				self.myPathMp3 = ".\\Tempfile\\myTts" + str(self.fileCount)+".mp3"
				self.outTextChange(self.myPathMp3)
			except:
				if str(self.inputBox.toPlainText()).count(".") > 2 or str(self.inputBox.toPlainText()).count(" ") > 30:
					QMessageBox.information(self, "information", "Text is too long")
					return None
				else:
					myPyttsx3(self.inputBox.toPlainText(), int(self.rateSpin.value()*100))
					return None	
		except Exception as e:
			QMessageBox.information(self,'Information' ,"Error 3:" + str(e))
			return None

		# self.statusLabel.setText("Last time take: %s s" % str(round(time.time() - start_time, 2)))
		if str(self.inputBox.toPlainText()).count(".") > 2 or str(self.inputBox.toPlainText()).count(" ") > 30:
			os.startfile(self.myPathMp3)
		else:
			playsound.playsound(self.myPathMp3)
		self.functionFinished()


	def listenButtonM_Click(self):
		# start_time = time.time()
		try:
			myPyttsx3(self.inputBox.toPlainText(), int(self.rateSpin.value()*100))
			return None
		except :
			print("Error 10")
			return None


	def listenButton_Click(self):
		if self.streamMode == "G":
			self.listenButtonG_Click()
		else:
			self.listenButtonM_Click()


	def hideButton_Clicked(self):
		self.meaningdWindow.hide()
		self.hide()


	# def hide(self):
	# 	self.meaningdWindow.hide()
	# 	self.hide()


	def largeButton_Click(self):

		monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
		work_area = monitor_info.get("Work")

		heightMonitor = work_area[3]
		widthMonitor = work_area[2]
		if self.height() <=200:
			self.inputBox.show()
			self.inputBoxRaw.hide()
			self.setFixedSize(250, heightMonitor-100)
			self.move(widthMonitor - self.width(), 40)
			self.outputBox.setFont(self.outputFont3)
		else:
			self.inputBox.hide()
			self.inputBoxRaw.show()
			mytext = (self.inputBox.toPlainText()).lower()
			mytext2 = re.sub("^\s+|\s+$", "", mytext, flags=re.UNICODE)
			if(mytext2 in myLingoesListWords):
				self.setFixedSize(400, 200)
				self.outputBox.setFont(self.outputFont3)
			else:
				self.setFixedSize(400, 150)
				self.outputBox.setFont(self.outputFont3)
			self.move(widthMonitor-400 , 40)

		self.meaningdWindow.hide()


	### Group3: Middlebar
	# Swap button

	def swapButton_Clicked(self):

		tempVarCombo1 = self.inputLabel.text()

		# print(tempVarCombo1)

		# reverse lang combobox
		self.inputLabel.setText(self.outputLabel.text())
		self.outputLabel.setText(tempVarCombo1)

		#reverse plantext form editTextbox

		tempVarEditBox1 = self.inputBox.toPlainText()
		self.inputBox.setText(self.outputBox.toPlainText())
		# self.outputBox.setPlainText(tempVarEditBox1)

		self.fromSym = myLangDict[self.inputLabel.text()]
		self.toSym = myLangDict[self.outputLabel.text()]

		self.transButton_Click()


	# Label status
	def functionStart(self):
		if self.isRunning == False:
			self.timeStart = time.time()
			self.statusLabel.setText("Running....")
			self.statusLabel.repaint()
			print(self.statusLabel.text())
			self.isRunning = True
		else:
			pass


	def functionFinished(self):
		if self.isRunning == True:
			self.timeFinished = time.time()
			self.statusLabel.setText("Finished: %ss" % str(round(self.timeFinished - self.timeStart, 1)))
			print(self.statusLabel.text())
			self.statusLabel.repaint()
			self.isRunning = False
		else:
			pass


	def functionNotSuccess(self):
		if self.isRunning == True:
			self.statusLabel.setText("Error")
			print(self.statusLabel.text())
			self.statusLabel.repaint()
			self.isRunning = False
		else:
			pass


	# Expand status
	def expandButton_Click(self):

		if self.height() >200:
			self.meaningdWindow.move(self.x()-self.meaningdWindow.width(), self.y())
		else:
			self.meaningdWindow.move(self.x(), self.y()+self.height())



		if self.meaningdWindow.inputWord.count(" ") <2:
			print("too long")
			if self.meaningdWindow.isHidden():
				self.meaningdWindow.show()

				self.meaningdWindow.refeshMeaningButton_click()
			else:
				self.meaningdWindow.hide()
		else:
			pass



	def refreshMeaningWindow(self):
		self.meaningdWindow.refeshMeaningButton_click()
		


	# def addToDbButton_Click(self):

	# 	nameCol1 = self.inputLabel.text()

	# 	nameCol2 = self.outputLabel.text()

	# 	inputText = str(self.inputBox.toPlainText())
	# 	outputText = str(self.outputBox.toPlainText())

	# 	if(inputText == None or inputText == "" or outputText == None or outputText ==""):
	# 		QMessageBox.information(self, "Information", "Không cho phép nhập vào database dữ liệu rỗng (Null, None)")
	# 		# print("Khong thanh cong")
	# 	else:
	# 		try:
	# 			if nameCol1=="English":
	# 				checkText = inputText
	# 			else:
	# 				checkText=outputText

	# 			if checkExitsRecord(checkText):
	# 				updateData = QMessageBox.question(self, 'Question', "Dữ liệu đã tồn tại, ghi đè?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
	# 				if updateData == QMessageBox.Yes:
	# 					if nameCol1=="English":
	# 						updateARow(inputText, outputText)
	# 						QMessageBox.information(self, "Information", "Cập nhật dữ liệu vào thành công")
	# 					else:
	# 						updateARow(outputText, inputText)
	# 						QMessageBox.information(self, "Information", "Cập nhật dữ liệu vào thành công")
	# 				else:
	# 					pass
	# 			else:
	# 				insertWord2DbEV(nameCol1, nameCol2, inputText, outputText)
	# 				QMessageBox.information(self, "Information", "Thêm dữ liệu vào thành công")
	# 		except Exception as e:
	# 			QMessageBox.information(self, "Information", str(e))

# # Autorun program 
# if __name__ == '__main__':
# 	import sys

# 	from PyQt5.QtWidgets import QApplication
# 	import os

# 	os.makedirs('.\\Tempfile', exist_ok = True)
# 	os.makedirs('.\\Capture', exist_ok = True)
# 	app = QApplication(sys.argv)
# 	app.setWindowIcon(QIcon('Icon.ico'))
# 	# Set style
# 	fileStyle = open(".\Resources\\Styles\\styleWindow.css").read()
# 	app.setStyleSheet(fileStyle)

# 	tempFolder = ".\\Tempfile"
# 	# Delete all tempfile
# 	for the_file in os.listdir(tempFolder):
# 		file_path = os.path.join(tempFolder, the_file)
# 		try:
# 			if os.path.isfile(file_path):
# 				os.unlink(file_path)
# 		except Exception as e:
# 			print(e)

# 	transTool = TranslateMainWindow()
# 	transTool.tray_icon.showMessage("Notification", "\nRight click to enable Autotranslate, Hide or Quit",QSystemTrayIcon.Information,3000)
# 	transTool.show()

# 	sys.exit(app.exec_())

        