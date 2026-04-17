
# -*- coding: utf-8 -*-
"""Sample PyQt5 app to demonstrate keybinder capabilities."""

import sys
# funtion freeze_support for make file exe without error
from multiprocessing import freeze_support

import time
import psutil    

import os
import platform
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QAbstractNativeEventFilter, QAbstractEventDispatcher

from PyQt5.QtWidgets import qApp, QApplication, QMessageBox

# Fix for direct execution/debugging: ensure 'src' is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, ".."))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from fake_lingoes.ui.main_window import TranslateMainWindow
from fake_lingoes.utils.path_helper import get_resource_path
from fake_lingoes import __version__

from pyqtkeybind import keybinder

class NativeEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0

if __name__ == '__main__':
    # Force X11 platform on Linux to ensure hotkey compatibility (QX11Info)
    if platform.system() == "Linux":
        os.environ["QT_QPA_PLATFORM"] = "xcb"

    # Put follow line to compile with pyinstaller
    freeze_support()

    # Create directories relative to current working directory
    os.makedirs('tempfile', exist_ok=True)
    os.makedirs('capture', exist_ok=True)
    
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    # Prevent app from exiting when window is hidden (minimize to tray)
    app.setQuitOnLastWindowClosed(False)
    try:
        mySettingDict = {
            "Time_out":10,
            "quit":"Shift+Ctrl+Q",
            "transClipboard":"Alt+Q",
            "alwaysTop":"Alt+A",
            "OCROffline":"Alt+W",
            "OCROnline":"Alt+I",
            "Large":"Alt+Z",
            "Expand":"Alt+E",
            "F5Dic":"Alt+R",
            "Show":"Alt+S",
            "SpaceOCR_apiKey": None,
            "Oxford_appID" : None,
            "Oxford_appKey" : None,
        }
        
        config_path = get_resource_path(os.path.join("configuration", "configuration.cfg"))
        if os.path.exists(config_path):
            with open(config_path) as fileConfig:
                for line in fileConfig:
                    if line.count("|") == 2:
                        listLine = line.split("|")
                        mySettingDict[str(listLine[0])] = str(listLine[1])
        
        mySettingtupple = (
            int(mySettingDict["Time_out"]),
            mySettingDict["quit"],
            mySettingDict["alwaysTop"],
            mySettingDict["transClipboard"],
            mySettingDict["OCROffline"],
            mySettingDict["OCROnline"],
            mySettingDict["Large"],
            mySettingDict["Expand"],
            mySettingDict["F5Dic"],
            mySettingDict["Show"],
            mySettingDict["SpaceOCR_apiKey"],
            mySettingDict["Oxford_appID"],
            mySettingDict["Oxford_appKey"],
        )
        print(mySettingtupple)
    except Exception as e:
        print(f"Using default setting due to: {e}")

    try:
        style_path = get_resource_path(os.path.join("resources", "styles", "style_window.css"))
        if os.path.exists(style_path):
            fileStyle = open(style_path).read()
            app.setStyleSheet(fileStyle)
        else:
            print(f"Style file not found at: {style_path}")
    except Exception as e:
        print(f"Using default style due to: {e}")

    tempFolder = "tempfile"
    # Delete all tempfile
    for the_file in os.listdir(tempFolder):
        file_path = os.path.join(tempFolder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    # Main Window
    windowMain = TranslateMainWindow()
    windowMain.setWindowTitle(f"Fake Lingoes v{__version__}")

    


    # set parameter
    windowMain.SpaceOCR_apiKey = mySettingtupple[10]

    windowMain.Oxford_appID = mySettingtupple[11]
    windowMain.Oxford_appKey = mySettingtupple[12]

    print(windowMain.Oxford_appID)
    print(windowMain.Oxford_appKey)

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


    def closeCurrentApp():
        exit()

    # the shortcut
    keybinder.init()
    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[1], qApp.quit)
    

    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[2], alwaysTop)
    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[3], transClipboard)
    
    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[4], windowMain.captureAreaButton_click)
    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[5], windowMain.captureApiButton_click)
    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[6], windowMain.largeButton_Click)
    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[7], windowMain.expandButton_Click)

    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[8], windowMain.refreshMeaningWindow)
    keybinder.register_hotkey(windowMain.winId(), mySettingtupple[9], windowMain.showOrHide)

    # Install a native event filter to receive events from the OS
    native_event_filter = NativeEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(native_event_filter)

    # Check FakeLingoes already running
    numFake = 0
    process_names = ["Fake Lingoes.exe", "FakeLingoes", "python"]
    for program in psutil.process_iter(['name']):
        try:
            if program.info['name'] in process_names:
                # If python, check if it's our script (simplified for now)
                numFake += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    print(f"Number of instances found: {numFake}")
    # On Linux, multiple python processes are common, so we might need a better check
    # For now, we'll keep it simple or allow the user to manage instances on Linux
    if platform.system() == "Windows" and int(numFake) > 2:
        exit()

        



    windowMain.show()



    app.exec_()

    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[1])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[2])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[3])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[4])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[5])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[6])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[7])

    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[8])
    keybinder.unregister_hotkey(windowMain.winId(), mySettingtupple[9])

# if __name__ == '__main__':
#     main()