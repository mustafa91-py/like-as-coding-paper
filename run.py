from coding_paper.coding_paper import CodingPaper,asdict
from input_window.input_window import Window, Stage
from tkinter import *
import os

if __name__ == '__main__':
    root = Window()
    root.mainloop()
    print(Stage.config)
    config: dict = Stage.config
    config["amount"] = 5
    config["file_read"] = False
    fp = os.path.join(os.getcwd(), "garbage", f"{config.get('title')}.lacp")
    config["file_path"] = fp


    def save_exit():
        if not cp.file_read:
            cp.save_dict.space = asdict(cp.container)
            cp.save_dict.save()
        root_2.destroy()


    root_2 = Tk()
    root_2.protocol("WM_DELETE_WINDOW", save_exit)
    cp = CodingPaper(root_2, cp_config=config)
    cp.pack()
    root_2.mainloop()
