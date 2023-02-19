from tkinter import *


class TopFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super(TopFrame, self).__init__(parent, *args, **kwargs)
        self.lesson = Label(self)
        self.subject = Label(self)
        self.title = Label(self)
        self.lesson.pack()
        self.subject.pack()
        self.title.pack()


class InputFrame(TopFrame):
    def __init__(self, parent, *args, **kwargs):
        super(InputFrame, self).__init__(parent, *args, **kwargs)


if __name__ == '__main__':
    root = Tk()
    inputf = InputFrame(root)
    inputf.pack()
    root.mainloop()
