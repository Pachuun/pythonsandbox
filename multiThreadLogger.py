from queue import Queue
import threading


class MultiThreadLogger():
    def __init__(self):
        self.logQueue = Queue()
        thr = threading.Thread(target=self.print)
        thr.setDaemon(True)
        thr.start()

    def queueLog(self, msg):
        self.logQueue.put(msg)

    def print(self):
        while (True):
            next = self.logQueue.get(True)
            if (next != None):
                print(next)
