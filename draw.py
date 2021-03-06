import win32api
import win32con
import win32gui
import time
import threading
import globals


class Draw():
    def __init__(self):
        self.windowText = ""
        self.hWindow = ""
        self.coords = [0, 0]

        # New code: Create and start the thread
        thr = threading.Thread(target=self.main)
        thr.setDaemon(True)
        thr.start()

    def main(self):
        # get instance handle
        hInstance = win32api.GetModuleHandle()
        # the class name
        className = 'SimpleWin32'

        # create and initialize window class
        wndClass = win32gui.WNDCLASS()
        wndClass.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wndClass.lpfnWndProc = self.wndProc
        wndClass.hInstance = hInstance
        wndClass.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
        wndClass.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        wndClass.lpszClassName = className

        # register window class
        wndClassAtom = None
        try:
            wndClassAtom = win32gui.RegisterClass(wndClass)
        except Exception as e:
            globals.logger.queueLog(e)
            raise e

        exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT

        style = win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE

        hWindow = win32gui.CreateWindowEx(
            exStyle,
            wndClassAtom,
            None,  # WindowName
            style,
            10,  # x
            10,  # y
            1920,  # width
            1080,  # height
            None,  # hWndParent
            None,  # hMenu
            hInstance,
            None  # lpParam
        )
        self.hWindow = hWindow

        # Show & update the window
        win32gui.SetLayeredWindowAttributes(hWindow, 0x00ffffff, 255,
                                            win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
        win32gui.SetWindowPos(hWindow, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
                              | win32con.SWP_SHOWWINDOW)

        win32gui.ShowWindow(hWindow, win32con.SW_SHOWNORMAL)
        win32gui.UpdateWindow(hWindow)

        # New code: Create and start the thread
        # thr = threading.Thread(target=self.customDraw, args=(hWindow,))
        # thr.setDaemon(False)
        # thr.start()

        # Dispatch messages
        win32gui.PumpMessages()

    def sendExit(self):
        win32api.SendMessage(self.hWindow, win32con.WM_DESTROY, None, None)

    def sendDraw(self, coords):
        self.coords = coords

    def customDraw(self, hWindow):

        strOne = "SomeUser: This is test line one"
        strTwo = "SomeOtherUser: This is test line two"
        strThree = "AndAnother: This is test line three"
        strFour = "UserOne: This is test line four"
        strFive = "AndAgain: This is test line five"

        # queue(strOne)
        # queue(strTwo)
        # queue(strThree)
        # queue(strFour)
        # queue(strFive)

        self.windowText = strOne
        win32gui.RedrawWindow(hWindow, None, None, win32con.RDW_INVALIDATE |
                              win32con.RDW_ERASE)

    def wndProc(self, hWnd, message, wParam, lParam):
        if message == win32con.WM_PAINT:
            hDC, paintStruct = win32gui.BeginPaint(hWnd)
            m = self.coords
            red = win32api.RGB(255, 0, 0)  # Red
            rect = win32gui.GetClientRect(hWnd)
            win32gui.RedrawWindow(hWnd, rect, None, win32con.RDW_INVALIDATE)

            try:
                for x in range(10):
                    win32gui.SetPixel(hDC, m[0]+x, m[1], red)
                    win32gui.SetPixel(hDC, m[0]+x, m[1]+10, red)
                    for y in range(10):
                        win32gui.SetPixel(hDC, m[0], m[1]+y, red)
                        win32gui.SetPixel(hDC, m[0]+10, m[1]+y, red)
            except:
                globals.logger.queueLog(
                    f"pizdec vsemu m[{m[0]},{m[1]}]")
                # raise

            win32gui.EndPaint(hWnd, paintStruct)
            return 0

        elif message == win32con.WM_DESTROY:
            globals.logger.queueLog('Being destroyed')
            win32gui.PostQuitMessage(0)
            return 0

        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)
