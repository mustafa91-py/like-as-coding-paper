import folder_operations
from coding_paper.coding_paper import CodingPaper, asdict, CodingPaperOpen
from input_window.input_frame import InputFrame
from tkinter import *
import folder_operations as fop
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
        cp.pack()
        self.protocol("WM_DELETE_WINDOW", save_exit)

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
    exit()
    root_2 = Tk()

    toolTips = ToolTip()
    root_2.wm_attributes("-topmost", 1)


    def okay():
        input_f.take_kwargs()
        kwargs = input_f.out_kw
        file_name = f"{kwargs.get('lesson')}_{kwargs.get('subject')}_{kwargs.get('title')}"
        file_path = os.path.join(folder_operations.F_P, file_name + ".json")
        kwargs.update(dict(file_path=file_path))

        def save_exit():
            cp.save_dict.space = asdict(cp.container)
            cp.save_dict.save()
            root_2.destroy()

        root_2.protocol("WM_DELETE_WINDOW", save_exit)
        cp = CodingPaper(root_2, cp_config=kwargs)
        cp.pack()


    input_f = InputFrame(root_2)
    input_f.pack()
    input_f.create_paper.configure(command=okay)

    root_2.mainloop()
