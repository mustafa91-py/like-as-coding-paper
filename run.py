from coding_paper.coding_paper import CodingPaper,asdict
from input_window.input_window import Window, Stage,InputFrame
from tkinter import *
import folder_operations as fop
import os

if __name__ == '__main__':

    def save_exit():
        cp.save_dict.space = asdict(cp.container)
        cp.save_dict.save()
        root_2.destroy()


    root_2 = Tk()
    ipf = InputFrame(root_2)
    ipf.pack()
    root_2.protocol("WM_DELETE_WINDOW", save_exit)
    cp = CodingPaper(root_2, cp_config=config)
    cp.pack()
    root_2.mainloop()
