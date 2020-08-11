import win32gui


class WindowsUtils():

    def getWindowHandleByName(self, name):
        toplist, winlist = [], []

        def enum_cb(hwnd, results):
            winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
        win32gui.EnumWindows(enum_cb, toplist)

        firefox = [(hwnd, title)
                   for hwnd, title in winlist if name in title.lower()]
        # just grab the hwnd for first window matching firefox
        firefox = firefox[0]
        hwnd = firefox[0]

        return hwnd

    def getForegroundWindowText(self):
        handle = win32gui.GetForegroundWindow()
        bbox = win32gui.GetWindowRect(handle)
        text = win32gui.GetWindowText(handle)
        return f"Foreground window - [name: {text}, handle: {handle}, bbox: {bbox}]"
