from PIL import ImageGrab
from input import KeyAsyncReader
from windows import WindowsUtils
from draw import Draw
import win32gui


class Process():
    def __init__(self, procName, exitChar="d"):
        self.reader = KeyAsyncReader()
        self.exitChar = ""
        self.reader.startReading(self.readCallback)
        self.windows = WindowsUtils()
        handle = self.windows.getWindowHandleByName(procName)
        self.draw = Draw()
        while True:
            # win32gui.SetForegroundWindow(handle)
            bbox = win32gui.GetWindowRect(handle)

            if self.exitChar == exitChar:
                self.draw.sendExit()
                break

    def readCallback(self, char):
        self.exitChar = char
