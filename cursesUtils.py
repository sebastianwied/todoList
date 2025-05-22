import curses as c
import curses.textpad as textpad

def createInputBox(uly, ulx, leny, lenx, stdscr, attrs=0):
    win = c.newwin(leny-2, lenx-3, uly+1, ulx+1)
    textpad.rectangle(stdscr, uly, ulx, uly+leny-1, ulx+lenx-2)
    tbox = textpad.Textbox(win, True)
    return win, (uly, ulx), tbox, lambda x,y: (ulx < x < ulx+lenx) and (uly < y < uly + leny)

def createBox(uly, ulx, leny, lenx, attrs=0, rect=True):
    win = c.newwin(leny, lenx, uly, ulx)
    if rect: textpad.rectangle(win, 0, 0, leny-1, lenx-2)
    return win, (uly, ulx), lambda x,y: ulx <= x <= ulx+lenx and uly <= y <= uly+leny

def createLabel(uly, ulx, label, attrs=0, rect=True):
    labelBox, _, boundCheck = createBox(uly, ulx, 3, len(label)+3, rect=rect)

    labelBox.addstr(1,1,label, attrs)
    return labelBox, (uly, ulx), boundCheck

class CursesObjectHandler:
    def __init__(self, stdscr):
        self.priority = [[stdscr],[], []]
        self.windows = dict()
        self.bounds = dict()
        self.tboxes = dict()
        self.topleft = dict()

    def assign(self, label, priority,
               window, bounds, tbox, topleft):
        self.priority[priority].append(window)
        self.windows[label] = window
        if bounds: self.bounds[label] = bounds
        if tbox: self.tboxes[label] = tbox
        self.topleft[label] = topleft

    def refreshWindows(self):
        for level in self.priority:
            for win in level:
                win.noutrefresh()
        c.doupdate()

    def checkBounds(self, mx, my):
        for bound in self.bounds.items():
            if bound[1](mx, my): return bound[0]
        return None