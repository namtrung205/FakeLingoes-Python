import os
import sys

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # In development, use the absolute path of the project root
        # This assumes path_helper.py is in src/fake_lingoes/utils/
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

    return os.path.join(base_path, relative_path)
