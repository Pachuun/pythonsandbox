import threading
import win32api
import win32console


class KeyAsyncReader():
    def __init__(self):
        self.stopLock = threading.Lock()
        self.stopped = True
        self.capturedChars = ""

        self.readHandle = win32console.GetStdHandle(win32api.STD_INPUT_HANDLE)
        self.readHandle.SetConsoleMode(
            win32console.ENABLE_LINE_INPUT | win32console.ENABLE_ECHO_INPUT | win32console.ENABLE_PROCESSED_INPUT)

    def startReading(self, readCallback):
        self.stopLock.acquire()

        try:
            if not self.stopped:
                raise Exception("Capture is already going")

            self.stopped = False
            self.readCallback = readCallback

            backgroundCaptureThread = threading.Thread(
                target=self.backgroundThreadReading)
            backgroundCaptureThread.daemon = True
            backgroundCaptureThread.start()
        except:
            self.stopLock.release()
            raise

        self.stopLock.release()

    def backgroundThreadReading(self):
        curEventLength = 0
        while True:
            eventsPeek = self.readHandle.PeekConsoleInput(10000)

            self.stopLock.acquire()
            if self.stopped:
                self.stopLock.release()
                return
            self.stopLock.release()

            if len(eventsPeek) == 0:
                continue

            if not len(eventsPeek) == curEventLength:
                if self.getCharsFromEvents(eventsPeek[curEventLength:]):
                    self.stopLock.acquire()
                    self.stopped = True
                    self.stopLock.release()
                    break

                curEventLength = len(eventsPeek)

    def getCharsFromEvents(self, eventsPeek):
        callbackReturnedTrue = False
        for curEvent in eventsPeek:
            if curEvent.EventType == win32console.KEY_EVENT:
                if ord(curEvent.Char) == 0 or not curEvent.KeyDown:
                    pass
                else:
                    curChar = str(curEvent.Char)
                    if self.readCallback(curChar) == True:
                        callbackReturnedTrue = True

        return callbackReturnedTrue

    def stopReading(self):
        self.stopLock.acquire()
        self.stopped = True
        self.stopLock.release()
