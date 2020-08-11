from PIL import ImageGrab
from input import KeyAsyncReader
from windows import WindowsUtils
from draw import Draw
import win32gui
import win32com.client
from pynput.mouse import Controller
import threading
import globals


class Process():
    def __init__(self, exitChar="d"):
        self.stopLock = threading.Lock()
        self.reader = KeyAsyncReader()
        self.exitChar = ""
        self.reader.startReading(self.readCallback)
        self.windows = WindowsUtils()
        mouse = Controller()
        self.draw = Draw()
        while True:
            try:
                #shell = win32com.client.Dispatch("WScript.Shell")
                # shell.SendKeys('%')
                handle = win32gui.GetForegroundWindow()
                bbox = win32gui.GetWindowRect(handle)
                self.stopLock.acquire()
                globals.logger.queueLog(handle)
                globals.logger.queueLog(bbox)
                self.stopLock.release()
                self.draw.sendDraw(mouse.position)
                if self.exitChar == exitChar:
                    self.draw.sendExit()
                    break
            except win32gui.error:
                break

    def readCallback(self, char):
        self.exitChar = char
