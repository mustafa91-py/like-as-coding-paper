from tkinter import *
from .imageforwidget import ImageForTkinter


class TopFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(TopFrame, self).__init__(parent, *args, **kwargs)


class PopUpWindow(Toplevel):
    def __init__(self):
        super(PopUpWindow, self).__init__()
