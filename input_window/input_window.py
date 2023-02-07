from tkinter import *
from tkinter import ttk


class InputFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(InputFrame, self).__init__(parent, *args, **kwargs)
        self.lesson_lbl = Label(self, text="lesson")
        self.lesson_lbl.grid(row=0, column=0)
        self.lesson_cbox = ttk.Combobox(self)
        self.lesson_cbox.grid(row=0, column=1)

        self.subject_lbl = Label(self, text="subject")
        self.subject_lbl.grid(row=1, column=0)
        self.subject_cbox = ttk.Combobox(self)
        self.subject_cbox.grid(row=1, column=1)

        self.name_ = Label(self, text="name")
        self.name_.grid(row=2, column=0)
        self.name_entry = Entry(self)
        self.name_entry.grid(row=2, column=1)


class Window(Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.top_frame = InputFrame(self)
        self.top_frame.pack()


if __name__ == '__main__':
    root = Window()
    root.mainloop()
