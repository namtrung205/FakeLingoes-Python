#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample PyQt5 app to demonstrate keybinder capabilities."""

import sys

import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher

from PyQt5.QtWidgets import qApp, QApplication

from UIMainWindow import TranslateMainWindow


from pyqtkeybind import keybinder


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


# def main():
#     app = QtWidgets.QApplication(sys.argv)
#     window = TranslateMainWindow()
#     # window = QtWidgets.QMainWindow()

#     print("Press Ctrl+Shift+A any where. Ctrl+Shift+E exits the app.")

#     # Setup a global keyboard shortcut to print "Hello World" on pressing
#     # the shortcut
#     keybinder.init()

#     def callback():
#         window.captureAreaButton_click()
#     def exit_app():
#         window.close()
#     keybinder.register_hotkey(window.winId(), "Shift+Ctrl+A", callback)
#     # keybinder.register_hotkey(window.winId(), "Shift+Ctrl+E", exit_app)
#     keybinder.register_hotkey(window.winId(), "Shift+Ctrl+E", qApp.quit)

#     # Install a native event filter to receive events from the OS
#     win_event_filter = WinEventFilter(keybinder)
#     event_dispatcher = QAbstractEventDispatcher.instance()
#     event_dispatcher.installNativeEventFilter(win_event_filter)

#     window.show()
#     app.exec_()
#     keybinder.unregister_hotkey(window.winId(), "Shift+Ctrl+A")
#     keybinder.unregister_hotkey(window.winId(), "Shift+Ctrl+E")


if __name__ == '__main__':

    os.makedirs('.\\Tempfile', exist_ok = True)
    os.makedirs('.\\Capture', exist_ok = True)
    # app.setWindowIcon(QIcon('Icon.ico'))
    # Set style
    app = QApplication(sys.argv)
    try:
        mySettingDict = {
            "Time_out":10,

            "quit":"Shift+Ctrl+Q",
            "transClipboard":"Alt+Q",
            "alwaysTop":"Alt+A",
            "OCROffline":"Alt+W",
            "OCROnline":"Alt+I"
        }
        with open(".\Configuration\\configuration.cfg") as fileConfig:
            for line in fileConfig:
                if line.count("|") ==2:
                    listLine = line.split("|")
                    mySettingDict[str(listLine[0])] = str(listLine[1])
                else:
                    pass
        mySettingtupple =(
            int(mySettingDict["Time_out"]),
            mySettingDict["quit"],
            mySettingDict["alwaysTop"],
            mySettingDict["transClipboard"],
            mySettingDict["OCROffline"],
            mySettingDict["OCROnline"],
        )
        print(mySettingtupple)
    except:
        print("Using default setting")

    try:
        fileStyle = open(".\Resources\\Styles\\styleWindow.css").read()
        app.setStyleSheet(fileStyle)
    except:
        print("Using default style")

    tempFolder = ".\\Tempfile"
    # Delete all tempfile
    for the_file in os.listdir(tempFolder):
        file_path = os.path.join(tempFolder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    windowMain = TranslateMainWindow()

    def alwaysTop():
        if windowMain.show_action.isChecked():
            windowMain.show_action.setChecked(False)
            windowMain.alwayTop_enable()
        else:
            windowMain.show_action.setChecked(True)
            windowMain.alwayTop_enable()

    def transClipboard():
        if windowMain.trans_clipboard_action.isChecked():
            windowMain.trans_clipboard_action.setChecked(False)
        else:
            windowMain.trans_clipboard_action.setChecked(True)


    # the shortcut
    keybinder.init()
    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[1], qApp.quit)
    

    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[2], alwaysTop)
    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[3], transClipboard)
    
    keybinder.register_hotkey(windowMain.winId(),mySettingtupple[4], windowMain.captureAreaButton_click)
    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[5], windowMain.captureApiButton_click)


    # Install a native event filter to receive events from the OS
    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    windowMain.show()
    app.exec_()

    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[1])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[2])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[3])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[4])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[5])


# if __name__ == '__main__':
#     main()