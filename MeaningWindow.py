# -*- coding: utf-8 -*-

from PyQt5.QtCore import QFile, QIODevice, Qt, QTextStream, QEvent, QSize,QPoint

from PyQt5.QtGui import QIcon, QShortcutEvent, QKeySequence, QFont, QPixmap
from PyQt5.QtWidgets import (QStyleOptionComboBox, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QMessageBox,
		QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QComboBox, QRadioButton, QCheckBox,
		QWidget, QShortcut, QApplication,QSystemTrayIcon,QStyle,QAction,qApp, QMenu, QDesktopWidget, QTabWidget, QDoubleSpinBox)

import os

from myStranslator import *

from gtts import gTTS
from gtts.tts import gTTSError
import playsound

import ctypes
import time



from win32api import GetMonitorInfo, MonitorFromPoint


from OxFordAPI import OxFordDic, WordNotFound

from SoHoaDict import SoHoaDic

from customeWidgets import *

# from myTimers import myTimer



class MeaningWindow(QWidget):
	"""docstring for TranslateTool"""
	# Font
	timeStart = 0.00
	timeFinished = 0.00
	# out Font
	outputFont1 = QFont()
	outputFont1.setPointSize(10)

	outputFont2 = QFont()
	outputFont2.setPointSize(14)
	# inputFont.setBold()


	def __init__(self, word="",parent = None):
		super(MeaningWindow, self).__init__(parent)

		self.inputWord = word

		### WINDOW
		#Icon Window:
		self.setWindowTitle("Fake Lingoes-UI")
		# Window flag
		self.setWindowFlags(
		Qt.Window |
		Qt.CustomizeWindowHint |
		Qt.WindowStaysOnTopHint |
		Qt.Tool|
		Qt.FramelessWindowHint
		)

		self.setWindowOpacity(0.9)

		self.setFixedSize(400,300)


		self.oldPos = self.pos()


		# Tabs OxFord
		# self.tabMeanEn = QWidget()
		# Mean EditBox
		self.meaningBoxEn = QTextEdit()
		self.meaningBoxEn.setFont(self.outputFont1)
		# print(self.meaningBoxEn.verticalScrollBar())

		self.meaningBoxVi = QTextEdit()
		self.meaningBoxVi.setFont(self.outputFont1)
		self.meaningBoxVi.hide()

		self.tabsOxF = QTabWidget()
		self.tabsOxF.hide()
		self.tabsOxF.setTabShape(1)
		self.tabsOxF.setTabPosition(1)

		self.tabEn = QWidget()
		# self.tabEn.hide()
		
		self.tabEn.layout = QVBoxLayout()
		self.tabEn.layout.setContentsMargins(0,0,0,0)
		self.tabEn.layout.addWidget(self.meaningBoxEn)
		self.tabEn.setLayout(self.tabEn.layout)


		self.tabVi = QWidget()
		# self.tabVi.hide()
		self.tabVi.layout = QVBoxLayout()
		self.tabVi.layout.setContentsMargins(0,0,0,0)
		self.tabVi.layout.addWidget(self.meaningBoxVi)
		self.tabVi.setLayout(self.tabVi.layout)


		self.tabsOxF.addTab(self.tabEn, 'English')
		# self.tabsOxF.addTab(self.tabVi, 'Vietnamese')

		# Tabs So Hoa
		# self.tabMeanEn = QWidget()

		self.meaningBoxEnSoHoa = QTextEdit()
		self.meaningBoxEnSoHoa.setFont(self.outputFont1)

		self.meaningBoxViSoHoa = QTextEdit()
		self.meaningBoxViSoHoa.setFont(self.outputFont1)


		self.meaningBoxEn_ViSoHoa = QTextEdit()
		self.meaningBoxEn_ViSoHoa.setFont(self.outputFont1)


		self.tabsSoHoa = QTabWidget()
		# self.tabsSoHoa.show()
		self.tabsSoHoa.setTabShape(1)
		self.tabsSoHoa.setTabPosition(1)


		self.tabViSoHoa = QWidget()
		self.tabViSoHoa.layout = QVBoxLayout()
		self.tabViSoHoa.layout.setContentsMargins(0,0,0,0)
		self.tabViSoHoa.layout.addWidget(self.meaningBoxViSoHoa)
		self.tabViSoHoa.setLayout(self.tabViSoHoa.layout)


		self.tabEnSoHoa = QWidget()
		self.tabEnSoHoa.layout = QVBoxLayout()
		self.tabEnSoHoa.layout.setContentsMargins(0,0,0,0)
		self.tabEnSoHoa.layout.addWidget(self.meaningBoxEnSoHoa)
		self.tabEnSoHoa.setLayout(self.tabEnSoHoa.layout)


		self.tabEn_ViSoHoa = QWidget()
		# self.tabEn_ViSoHoa.hide()
		self.tabEn_ViSoHoa.layout = QVBoxLayout()
		self.tabEn_ViSoHoa.layout.setContentsMargins(0,0,0,0)
		self.tabEn_ViSoHoa.layout.addWidget(self.meaningBoxEn_ViSoHoa)
		self.tabEn_ViSoHoa.setLayout(self.tabEn_ViSoHoa.layout)

		self.tabsSoHoa.addTab(self.tabViSoHoa, 'SoHoaE-V')
		self.tabsSoHoa.addTab(self.tabEnSoHoa, 'SoHoaE-E')
		# self.tabsSoHoa.addTab(self.tabEn_ViSoHoa, 'EN--->VI')


		# Button botbar

		self.addToDbButton = myIconButton()
		iconaddToDb = QIcon()
		iconaddToDb.addPixmap(QPixmap(".\\Resources\\Images\\import.png"))
		self.addToDbButton.setFlat(True)
		self.addToDbButton.setIcon(iconaddToDb)
		self.addToDbButton.setIconSize(QSize(20,20))
		self.addToDbButton.setFixedHeight(20)
		self.addToDbButton.setToolTip("Add to database")

		self.refeshMeaningButton = myIconButton()
		iconfreshMean = QIcon()
		iconfreshMean.addPixmap(QPixmap(".\\Resources\\Images\\refresh.png"))
		self.refeshMeaningButton.setFlat(True)
		self.refeshMeaningButton.setIcon(iconfreshMean)
		self.refeshMeaningButton.setIconSize(QSize(20,20))
		self.refeshMeaningButton.setFixedHeight(20)
		self.refeshMeaningButton.setToolTip("Fresh shower")

		self.transMeaningButton = myIconButton()
		self.transMeaningButton.hide()
		icontransMean = QIcon()
		icontransMean.addPixmap(QPixmap(".\\Resources\\Images\\transMeaning.png"))
		self.transMeaningButton.setFlat(True)
		self.transMeaningButton.setIcon(icontransMean)
		self.transMeaningButton.setIconSize(QSize(20,20))
		self.transMeaningButton.setFixedHeight(20)
		self.transMeaningButton.setToolTip("Translate meaning")

		self.dictComBo = QComboBox()
		self.dictComBo.addItem("So Hoa")
		self.dictComBo.addItem("OxFord")
		self.dictComBo.setFixedWidth(75)
		# print(self.dictComBo.initStyleOption)
		# self.dictComBo.

		self.isRunning = False
		self.statusLabel = QLabel("No Notification.")
		self.statusLabel.setFixedWidth(120)
		

		# bottom bar

		botBarLayout = QHBoxLayout()
		botBarLayout.setContentsMargins(0,-2,0,0)
		botBarLayout.addWidget(self.refeshMeaningButton)
		botBarLayout.addSpacing(10)
		botBarLayout.addWidget(self.transMeaningButton)
		botBarLayout.addSpacing(20)
		botBarLayout.addWidget(self.dictComBo)
		botBarLayout.addSpacing(20)
		botBarLayout.addWidget(self.statusLabel)

		botBarLayout.addStretch()
		botBarLayout.addWidget(self.addToDbButton)
		botBarLayout.addSpacing(5)

		#  mainLayout

		mainLayout = QVBoxLayout()
		mainLayout.setContentsMargins(0,0,0,0)
		# mainLayout.addWidget(self.meaningBoxEn)
		mainLayout.addWidget(self.tabsOxF)
		mainLayout.addWidget(self.tabsSoHoa)

		mainLayout.addSpacing(-5)
		mainLayout.addLayout(botBarLayout)
		mainLayout.addSpacing(2)
		self.setLayout(mainLayout)

		# connect
		self.dictComBo.currentTextChanged.connect(self.currentDict_change)
		self.refeshMeaningButton.clicked.connect(self.refeshMeaningButton_click)
		self.transMeaningButton.clicked.connect(self.transMeaningButton_click)



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


	def transMeaningButton_click(self):
		print("transMean click")
		self.functionStart()
		self.transMeaningButton.hide()
		try:
			if self.dictComBo.currentText() == "So Hoa":
				self.tabsSoHoa.addTab(self.tabEn_ViSoHoa, 'EN--->VI')				
				self.tabEn_ViSoHoa.show()				

				SoHoaEn_EnHtml = "<h2>%s</h2>" %self.inputWord + SoHoaDic().getFullHtml(self.inputWord,"en_en")
				print("Chieu dai html")
				print(len(SoHoaEn_EnHtml))
				if len(SoHoaEn_EnHtml) > 10000:
					SoHoaEn_EnHtml = SoHoaEn_EnHtml[0:9999]
				print(len(SoHoaEn_EnHtml))
				self.meaningBoxEn_ViSoHoa.setPlainText("")
				transMeanEnToVi = googleTrans(SoHoaEn_EnHtml, "en", "vi")
				transMeanEnToViHtml = transMeanEnToVi.replace("/ ", "/")
				self.meaningBoxEn_ViSoHoa.textCursor().insertHtml(transMeanEnToViHtml)
			elif self.dictComBo.currentText() == "OxFord":
				self.meaningBoxVi.show()
				self.meaningBoxVi.setPlainText("")
				
				self.tabsOxF.addTab(self.tabVi, "EN--->VI")
				self.tabVi.show()
				transMeanToVi = googleTrans(OxFordDic().getHtml(self.inputWord), "en", "vi")
				# print(transMeanToVi)
				transMeanToViHtml = transMeanToVi.replace("/ ", "/")
				# transMeanToVi = str(googleTrans(OxFordDic().getHtml(self.inputWord), 'en', 'vi')).replace("/ ", "/")
				self.meaningBoxVi.textCursor().insertHtml(transMeanToViHtml)
			else:
				pass
	
		except:
			print("Error")
		self.functionFinished()


	def refeshMeaningButton_click(self):
		self.functionStart()
		try: 
			self.transMeaningButton.show()
			print("f5 clicked")
			if self.dictComBo.currentText() =="OxFord":
				self.tabsOxF.removeTab(1)
				self.tabVi.hide()
				self.meaningBoxEn.setPlainText("")

				self.meaningBoxEn.textCursor().insertHtml(OxFordDic().getHtml(self.inputWord))

				# transMeanToVi = googleTrans(OxFordDic().getHtml(self.inputWord), "en", "vi")
				# transMeanToViHtml = transMeanToVi.replace("/ ", "/")
				# # transMeanToVi = str(googleTrans(OxFordDic().getHtml(self.inputWord), 'en', 'vi')).replace("/ ", "/")
				# self.meaningBoxVi.textCursor().insertHtml(transMeanToViHtml)

			elif self.dictComBo.currentText() == "So Hoa":
				self.tabsSoHoa.removeTab(2)
				# self.meaningBoxViSoHoa.setPlainText("helo")
				self.meaningBoxViSoHoa.setPlainText("")
				self.meaningBoxViSoHoa.textCursor().insertHtml("<h2>%s</h2>" %self.inputWord + SoHoaDic().getFullHtml(self.inputWord,"en_vi"))
				
				self.meaningBoxEnSoHoa.setPlainText("")
				SoHoaEn_EnHtml = "<h2>%s</h2>" %self.inputWord + SoHoaDic().getFullHtml(self.inputWord,"en_en")
				self.meaningBoxEnSoHoa.textCursor().insertHtml(SoHoaEn_EnHtml)

		except Exception as e:
			QMessageBox.information(self, "Information", str(e))
		self.functionFinished()			


	def currentDict_change(self):
		try:
			if self.dictComBo.currentText() == "OxFord":
				self.refeshMeaningButton_click()
				self.tabsOxF.show()
				self.tabsSoHoa.hide()

			elif self.dictComBo.currentText() == "So Hoa":
				self.refeshMeaningButton_click()
				self.tabsOxF.hide()
				self.tabsSoHoa.show()
			else:
				pass
		except Exception as e:
			QMessageBox.information(self, "Information", str(e))

	# Limit time
	
	# def transMeaningButton_click_limit(self):
	# 	myTimer(self.transMeaningButton_click,(), 20)

	# def refeshMeaningButton_click_limit(self):
	# 	myTimer(self.refeshMeaningButton_click,(), 20)

	# def currentDict_change_limit(self):
	# 	myTimer(self.currentDict_change,(), 20)





# # Autorun program 
# if __name__ == '__main__':
# 	import sys
# 	from PyQt5.QtWidgets import QApplication
# 	import os
# 	os.makedirs('.\\Tempfile', exist_ok = True)
# 	app = QApplication(sys.argv)
# 	app.setWindowIcon(QIcon('Icon.ico'))
# 	# Set style
# 	# fileStyle = open("styleWindow.css").read()
# 	# app.setStyleSheet(fileStyle)
# 	app.setStyleSheet("""
# 						MeaningWindow{background-color: rgb(109, 110, 106) ; border: 0px solid red;} 
# 						QTabWidget{background-color: rgb(109, 110, 106) ; border: 0px solid;} 
# 						QPtyWidget{background-color: rgb(109, 110, 106) ; border: 0px solid;} 
# 						QDoubleSpinBox{background-color: rgb(109, 110, 106) ; border: 1px solid rgb(100, 100, 89);}
# 						TranslateMainWindow{background-color: rgb(109, 110, 106) ; border: 10px solid red;}
# 						QScrollBar:vertical{background-color: rgba(255,255,255,0.5) ; border: None; width: 4px;}
# 						myIconButton{border: 0px solid;}
# 						QTextEdit{background-color: rgb(40, 50, 39); color: white; border: 1px solid black;}
# 						QLineEdit{background-color: rgb(40, 40, 39); color: white; border: 1px solid; border: 1px solid black;}
# 						QLabel{border: 0px solid;color: black;}
# 						""")

# 	tempFolder = ".\\Tempfile"
# 	# Delete all tempfile
# 	for the_file in os.listdir(tempFolder):
# 		file_path = os.path.join(tempFolder, the_file)
# 		try:
# 			if os.path.isfile(file_path):
# 				os.unlink(file_path)
# 		except Exception as e:
# 			print(e)

# 	transTool = MeaningWindow("construction")
# 	transTool.show()

# 	sys.exit(app.exec_())
