from tkinter import *


class TopFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super(TopFrame, self).__init__(parent, *args, **kwargs)
        self.lesson = Label(self, text="lesson")
        self.subject = Label(self, text="subject")
        self.title = Label(self, text="title")
        self.lesson.grid(row=0, column=0)
        self.subject.grid(row=1, column=0)
        self.title.grid(row=2, column=0)
        self.lesson_entry = Entry(self)
        self.subject_entry = Entry(self)
        self.title_entry = Entry(self)
        self.lesson_entry.grid(row=0, column=1)
        self.subject_entry.grid(row=1, column=1)
        self.title_entry.grid(row=2, column=1)


class MidFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super(MidFrame, self).__init__(parent, *args, **kwargs)
        self.amount = Label(self, text="amount")
        self.unit_per_minute = Label(self, text="unit per min")
        self.amount.grid(row=0, column=0)
        self.unit_per_minute.grid(row=1, column=0)
        self.amount_scale = Scale(self, resolution=1, orient=HORIZONTAL, length=200)
        self.amount_scale.grid(row=0, column=1)


class InputFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(InputFrame, self).__init__(parent, *args, **kwargs)
        self.topFrame = TopFrame(self)
        self.topFrame.pack()
        self.midFrame = MidFrame(self)
        self.midFrame.pack()


if __name__ == '__main__':
    root = Tk()
    inputf = InputFrame(root)
    inputf.pack()
    root.mainloop()
