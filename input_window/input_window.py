from tkinter import *
from tkinter import ttk


class Stage:
    config: dict = None


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

        self.title = Label(self, text="name")
        self.title.grid(row=2, column=0)
        self.title_entry_var = StringVar()
        self.title_entry = Entry(self, textvariable=self.title_entry_var)
        self.title_entry.grid(row=2, column=1)


class Window(Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.protocol("WM_DELETE_WINDOW", exit)
        self.top_frame = InputFrame(self)
        self.top_frame.pack()
        self.save = Button(self, text="save", command=self.get)
        self.save.pack()

    def get(self):
        out = dict(lesson=self.top_frame.lesson_cbox.get(),
                   subject=self.top_frame.subject_cbox.get(),
                   title=self.top_frame.title_entry_var.get())
        Stage.config = out
        self.destroy()


if __name__ == '__main__':
    from coding_paper.coding_paper import CodingPaper
    import os

    root = Window()
    root.mainloop()
    print(Stage.config)
    config: dict = Stage.config
    config["amount"] = 20
    config["file_read"] = False
    fp = os.path.join(os.getcwd(), "../garbage", f"{config.get('title')}.json")
    config["file_path"] = fp
    root_2 = Tk()
    cp = CodingPaper(root_2, cp_config=config)
    cp.pack()
    root_2.mainloop()
