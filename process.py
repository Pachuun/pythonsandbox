from PIL import ImageGrab
from input import KeyAsyncReader
from windows import WindowsUtils
from draw import Draw
import win32gui
import win32com.client
from pynput.mouse import Controller
import threading
import globals

import numpy as np
import cv2


class Process():
    def __init__(self, exitChar="d"):
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
                globals.logger.queueLog(self.windows.getForegroundWindowText())
                screen = self.windows.getForegroundWindowScreen()
                #im = cv2.imread(np.array(screen))
                gray = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)
                corners = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
                corners = np.int0(corners)
                for i in corners:
                    x, y = i.ravel()

                self.draw.sendDraw((x, y))
                if self.exitChar == exitChar:
                    self.draw.sendExit()
                    break
            except win32gui.error:
                break

    def readCallback(self, char):
        self.exitChar = char
