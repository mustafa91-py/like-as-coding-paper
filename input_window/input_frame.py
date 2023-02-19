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
        self.amount_var = DoubleVar()
        self.amount_scale = Scale(self, variable=self.amount_var,
                                  to=20, from_=1,
                                  resolution=1,
                                  orient=HORIZONTAL,
                                  length=250, command=self.try_command)
        self.amount_scale.grid(row=0, column=1)
        self.amount_scale.set(10)
        self.unit_per_minute_var = DoubleVar()
        self.unit_per_minute_scale = Scale(self, from_=.1, to=10, variable=self.unit_per_minute_var,
                                           resolution=.1, orient=HORIZONTAL, length=200, )
        self.unit_per_minute_scale.grid(row=1, column=1)
        self.unit_per_minute_scale.set(1)

    def try_command(self, value):
        current_to = self.amount_scale["to"]
        length_ = self.amount_scale["length"]
        if current_to >= 500:
            return
        percent = round((int(value) / float(current_to) * 100), 2)
        if percent >= 90:
            self.amount_scale.configure(to=current_to + 5, length=length_ + 5)
            self.amount_scale.set(value)
        self.unit_per_minute_scale.configure(length=self.amount_scale["length"])


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
