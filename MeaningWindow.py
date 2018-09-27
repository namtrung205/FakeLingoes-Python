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



from win32api import GetMonitorInfo, MonitorFromPoint


from OxFordAPI import OxFordDic, WordNotFound

from SoHoaDict import *

from customeWidgets import *






class MeaningWindow(QWidget):
	"""docstring for TranslateTool"""
	# Font

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
		self.setWindowTitle("Translator - UI ")
		# Window flag
		self.setWindowFlags(
		Qt.Window |
		Qt.CustomizeWindowHint |
		Qt.WindowStaysOnTopHint |
		Qt.FramelessWindowHint
		)

		self.setWindowOpacity(0.95)

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

		self.tabsOxF = QTabWidget()
		# self.tabsOxF.show()
		self.tabsOxF.setTabShape(1)
		self.tabsOxF.setTabPosition(1)

		self.tabEn = QWidget()
		self.tabEn.layout = QVBoxLayout()
		self.tabEn.layout.setContentsMargins(0,0,0,0)
		self.tabEn.layout.addWidget(self.meaningBoxEn)
		self.tabEn.setLayout(self.tabEn.layout)


		self.tabVi = QWidget()
		self.tabVi.layout = QVBoxLayout()
		self.tabVi.layout.setContentsMargins(0,0,0,0)
		self.tabVi.layout.addWidget(self.meaningBoxVi)
		self.tabVi.setLayout(self.tabVi.layout)


		self.tabsOxF.addTab(self.tabEn, 'English')
		self.tabsOxF.addTab(self.tabVi, 'Vietnamese')

		# Tabs So Hoa
		# self.tabMeanEn = QWidget()

		self.meaningBoxViSoHoa = QTextEdit()
		self.meaningBoxViSoHoa.setFont(self.outputFont1)


		self.tabsSoHoa = QTabWidget()
		self.tabsSoHoa.hide()
		self.tabsSoHoa.setTabShape(1)
		self.tabsSoHoa.setTabPosition(1)


		self.tabViSoHoa = QWidget()
		self.tabViSoHoa.layout = QVBoxLayout()
		self.tabViSoHoa.layout.setContentsMargins(0,0,0,0)
		self.tabViSoHoa.layout.addWidget(self.meaningBoxViSoHoa)
		self.tabViSoHoa.setLayout(self.tabViSoHoa.layout)

		self.tabsSoHoa.addTab(self.tabViSoHoa, 'SoHoaDict')


		# Button botbar

		self.addToDbButton = myIconButton()
		iconaddToDb = QIcon()
		iconaddToDb.addPixmap(QPixmap(".\\images\\import.png"))
		self.addToDbButton.setFlat(True)
		self.addToDbButton.setIcon(iconaddToDb)
		self.addToDbButton.setIconSize(QSize(20,20))
		self.addToDbButton.setFixedHeight(20)
		self.addToDbButton.setToolTip("Add to database")

		self.refeshMeaningButton = myIconButton()
		icontransMean = QIcon()
		icontransMean.addPixmap(QPixmap(".\\images\\refresh.png"))
		self.refeshMeaningButton.setFlat(True)
		self.refeshMeaningButton.setIcon(icontransMean)
		self.refeshMeaningButton.setIconSize(QSize(20,20))
		self.refeshMeaningButton.setFixedHeight(20)
		self.refeshMeaningButton.setToolTip("Fresh shower")

		self.dictComBo = QComboBox()
		self.dictComBo.addItem("OxFord")
		self.dictComBo.addItem("So Hoa")
		self.dictComBo.setFixedWidth(75)
		print(self.dictComBo.initStyleOption)
		# self.dictComBo.


		# bottom bar

		botBarLayout = QHBoxLayout()
		botBarLayout.setContentsMargins(0,-2,0,0)
		botBarLayout.addWidget(self.refeshMeaningButton)
		botBarLayout.addWidget(self.dictComBo)

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
		self.setLayout(mainLayout)

		# connect
		self.dictComBo.currentTextChanged.connect(self.currentDict_change)
		self.refeshMeaningButton.clicked.connect(self.refeshMeaningButton_click)




	def transMeaningButton_click(self):
		try:
			inTrans = str(self.meaningBoxEn.toPlainText())
			self.outputBox.setPlainText(googleTrans(inTrans, 'en', 'vi'))
		except Exception as e:
			QMessageBox.information(self, "Information", str(e) + "Lỗi 2.1")


	def refeshMeaningButton_click(self):
		try: 
			print("f5 clicked")
			if self.dictComBo.currentText() =="OxFord":
				self.meaningBoxEn.setPlainText("")
				self.meaningBoxVi.setPlainText("")
				self.meaningBoxEn.textCursor().insertHtml(OxFordDic().getHtml(self.inputWord))

				transMeanToVi = googleTrans(OxFordDic().getHtml(self.inputWord), "en", "vi")
				transMeanToViHtml = transMeanToVi.replace("/ ", "/")
				# transMeanToVi = str(googleTrans(OxFordDic().getHtml(self.inputWord), 'en', 'vi')).replace("/ ", "/")
				self.meaningBoxVi.textCursor().insertHtml(transMeanToViHtml)

				pass
				# In ra man hinh
			elif self.dictComBo.currentText() == "So Hoa":
				# self.meaningBoxViSoHoa.setPlainText("helo")
				self.meaningBoxViSoHoa.setPlainText("")
				self.meaningBoxViSoHoa.textCursor().insertHtml(SoHoaDic().getMean(self.inputWord))
		except Exception as e:
			QMessageBox.information(self, "Information", str(e))
			
		

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



# # Autorun program 
# if __name__ == '__main__':
# 	import sys
# 	from PyQt5.QtWidgets import QApplication
# 	import os
# 	os.makedirs('.\\Tempfile', exist_ok = True)
# 	app = QApplication(sys.argv)
# 	app.setWindowIcon(QIcon('Icon.ico'))
# 	# Set style
# 	fileStyle = open("styleWindow.css").read()
# 	app.setStyleSheet(fileStyle)
# 	# app.setStyleSheet("""
# 	# 					MeaningWindow{background-color: rgb(109, 110, 106) ; border: 0px solid red;} 
# 	# 					QTabWidget{background-color: rgb(109, 110, 106) ; border: 0px solid;} 
# 	# 					QPtyWidget{background-color: rgb(109, 110, 106) ; border: 0px solid;} 
# 	# 					QDoubleSpinBox{background-color: rgb(109, 110, 106) ; border: 1px solid rgb(100, 100, 89);}
# 	# 					TranslateMainWindow{background-color: rgb(109, 110, 106) ; border: 10px solid red;}
# 	# 					QScrollBar:vertical{background-color: rgba(255,255,255,0.5) ; border: None; width: 4px;}
# 	# 					myIconButton{border: 0px solid;}
# 	# 					QTextEdit{background-color: rgb(40, 50, 39); color: white; border: 1px solid black;}
# 	# 					QLineEdit{background-color: rgb(40, 40, 39); color: white; border: 1px solid; border: 1px solid black;}
# 	# 					QLabel{border: 0px solid;color: black;}
# 	# 					""")

# 	tempFolder = ".\\Tempfile"
# 	# Delete all tempfile
# 	for the_file in os.listdir(tempFolder):
# 		file_path = os.path.join(tempFolder, the_file)
# 		try:
# 			if os.path.isfile(file_path):
# 				os.unlink(file_path)
# 		except Exception as e:
# 			print(e)

# 	transTool = MeaningWindow("construction standard")
# 	transTool.show()

# 	sys.exit(app.exec_())
