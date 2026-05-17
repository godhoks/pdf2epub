import ctypes
import os
import sys
from gui import App

if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("PDF2EPUB.Converter.1")
    app = App()
    base = sys._MEIPASS if hasattr(sys, "_MEIPASS") else os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base, "icon.ico")
    if os.path.exists(icon_path):
        app.iconbitmap(icon_path)
    app.mainloop()
