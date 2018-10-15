from PyQt5.QtCore import QFile, QIODevice, Qt, QTextStream, QEvent, QSize,QPoint,QCoreApplication


from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QIcon, QShortcutEvent, QKeySequence, QFont, QPixmap
from PyQt5.QtWidgets import (QDialog, QFileDialog, QGridLayout, QHBoxLayout, QMessageBox,
		QLabel, QLineEdit , QPushButton, QTextEdit, QVBoxLayout, QComboBox, QRadioButton, QCheckBox,
		QWidget, QShortcut, QApplication,QSystemTrayIcon,QStyle,QAction,qApp, QMenu, QDesktopWidget, QTabWidget, QDoubleSpinBox)

import os
from PIL import ImageGrab
import time

from PIL import Image
from pytesseract import image_to_string
from customeWidgets import *
# Incon

class CaptureWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(30,30,600,400)
        self.setWindowOpacity(0.6)
        # MeaningWindow{background-color: rgb(99, 99, 99) ; border: 0px solid red;}
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        # self.show()
    
        self.capButton = QPushButton("", self)

        # self.capButton = myIconButton()
        # self.capButton.setParent(self)
        iconTrans = QIcon()
        iconTrans.addPixmap(QPixmap(".\Resources\\Images\\camera.png"))
        # self.capButton.setFlat(True)
        self.capButton.setIcon(iconTrans)
        self.capButton.setIconSize(QSize(30,30))
        self.capButton.setFixedSize(30, 30)
        self.capButton.setToolTip('Take shot')
        self.capButton.hide()
        # self.capButton.clicked.connect(self.capButton_click)

        self.capShortcut= QShortcut(QKeySequence("Space"),self)
        # self.capShortcut.activated.connect(self.capButton_click)
        self.cancelShortcut= QShortcut(QKeySequence("Escape"),self)

        self.p1 = QtCore.QPoint()
        self.p2=QtCore.QPoint()

        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showFullScreen()


    def capButton_click(self):
        self.a = (min(self.p1.x(),self.p2.x()) ,min(self.p1.y(),self.p2.y()) ,max(self.p1.x(),self.p2.x()), max(self.p1.y(),self.p2.y()))
        # print(self.a)
        self.hide()
        time.sleep(0.5)
        self.capture(self.a)
        # return (self.a)


    def capture(self,window):
        img = ImageGrab.grab(bbox=window)
        # img2 = ImageGrab.grabclipboard
        # print(img)
        img.save(".\Capture\\capture.png")



    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setOpacity(0.7)
        br = QtGui.QBrush(QtGui.QColor(225, 225, 10)) 
        pen = QtGui.QPen(QtGui.QColor(235, 0, 205), 1, Qt.SolidLine)
        
        qp.setPen(pen)
        qp.drawRect(QtCore.QRect(self.begin, self.end))


    def mousePressEvent(self, event):
        # if event.button() == QtCore.Qt.LeftButton:
        if event.button() == QtCore.Qt.LeftButton:

            self.begin = event.pos()
            # print(self.begin)
            self.p1 = self.begin
            self.end = event.pos()
            # self.update()
        else:
            pass

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()


    def mouseReleaseEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:        
            self.begin = event.pos()
            # print(self.begin)
            self.end = event.pos()
            # print(self.end)
            self.p2 = self.end
            self.capButton.show()
            self.capButton.move(self.p2.x(), self.p2.y())
            # self.update()
            # self.drawRectangle()

        else:
            pass



class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(30,30,600,400)

        # self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # self.captureAreaButton = QPushButton("Cap")
        self.captureAreaButton = myIconButton()
        self.captureAreaButton.setParent(self)
        selectAreaIcon = QIcon()
        selectAreaIcon.addPixmap(QPixmap(".\\Resources\\Images\\SelectArea.png"))
        self.captureAreaButton.setFlat(True)
        self.captureAreaButton.setIcon(selectAreaIcon)
        self.captureAreaButton.setIconSize(QSize(20,20))
        self.captureAreaButton.setFixedSize(20, 20)
        self.captureAreaButton.setToolTip('Translate')
        # self.captureAreaButton.hide()


        barLayout = QHBoxLayout()
        barLayout.addWidget(self.captureAreaButton)
        
        self.setLayout(barLayout)

        self.captureAreaButton.clicked.connect(self.captureAreaButton_click)

        self.wincap = CaptureWindow()
        self.wincap.hide()

        # connect

    def captureAreaButton_click(self):
        self.wincap.close()
        self.wincap = CaptureWindow()
        self.wincap.show()
        



        