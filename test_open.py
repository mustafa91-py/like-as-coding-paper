import os.path

import folder_operations
from coding_paper.coding_paper import CodingPaperOpen
from tkinter import *
from tkinter.filedialog import askopenfilename

if __name__ == '__main__':
    try:
        file_path = askopenfilename(initialdir=os.path.join(folder_operations.F_P))
        print(f"{file_path=}")
    except FileNotFoundError:
        file_path = os.path.join(folder_operations.F_P, "w_w_w.json")
    root = Tk()
    cp = CodingPaperOpen(root, file_path=file_path)
    cp.stain()
    root.wm_attributes("-topmost",1)
    print(cp.container.get_data())
    cp.pack(fill="both", expand=1)


    def save_exit():
        cp.save_dict.save()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", save_exit)


    # print(cp.container)
    root.mainloop()
