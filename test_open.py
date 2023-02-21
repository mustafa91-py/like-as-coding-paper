import os.path

import folder_operations
from coding_paper.coding_paper import CodingPaperOpen
from tkinter import *

if __name__ == '__main__':
    fff = os.path.join(folder_operations.F_P, "w_w_w.json")
    root = Tk()
    print(fff)
    cp = CodingPaperOpen(root, file_path=fff)
    cp.stain()
    print(cp.container.get_data())
    cp.pack(fill="both", expand=1)


    def save_exit():
        cp.save_dict.save()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", save_exit)


    # print(cp.container)
    root.mainloop()
