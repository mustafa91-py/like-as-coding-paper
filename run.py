import folder_operations
from coding_paper.coding_paper import CodingPaper, asdict, CodingPaperOpen
from input_window.input_frame import InputFrame
from tkinter import *
from tkinter.filedialog import askopenfilename
import os
from features.my_op_tooltip import ToolTip


class Run(Tk):
    def __init__(self):
        super().__init__()
        self.tooltips = ToolTip()
        self.wm_attributes("-topmost", 1)
        self.inputFrame = InputFrame(self)
        self.inputFrame.pack()
        self.inputFrame.create_paper.configure(command=self.coding_paper)
        self.menuBar = Menu()
        self.menuBar.add_command(label="open", command=self.file_open)
        self.configure(menu=self.menuBar)

    def get_input(self):
        kwargs = self.inputFrame.take_kwargs()
        file_name = f"{kwargs.get('lesson')}_{kwargs.get('subject')}_{kwargs.get('title')}"
        file_path = os.path.join(folder_operations.F_P, file_name + ".json")
        kwargs.update(dict(file_path=file_path))
        return kwargs

    def coding_paper(self):
        def save_exit():
            cp.save_dict.space = asdict(cp.container)
            cp.save_dict.save()
            self.destroy()

        cp = CodingPaper(self, cp_config=self.get_input())
        cp.pack(side="left")
        self.protocol("WM_DELETE_WINDOW", save_exit)
        self.configure(menu=Menu())

    def file_open(self):
        file_path = askopenfilename(initialdir=os.path.join(folder_operations.F_P))
        if os.path.exists(file_path):
            pass
        else:
            file_path = os.path.join(folder_operations.F_P, "w_w_w.json")
        cpo = CodingPaperOpen(self, file_path=file_path)
        cpo.pack(fill="both", expand=1)
        self.configure(menu=Menu())
        self.inputFrame.pack_forget()

        def save_exit():
            cpo.save_dict.save()
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", save_exit)


if __name__ == '__main__':
    root = Run()

    root.mainloop()
