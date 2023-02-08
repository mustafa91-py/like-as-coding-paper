from coding_paper.coding_paper import CodingPaper
from input_window.input_window import Window, Stage
from tkinter import *
import os

if __name__ == '__main__':
    root = Window()
    root.mainloop()
    print(Stage.date)
    config: dict = Stage.date
    config["amount"] = 20
    config["file_read"] = False
    fp = os.path.join(os.getcwd(), "garbage", f"{config.get('title')}.json")
    config["file_path"] = fp
    root_2 = Tk()
    cp = CodingPaper(root_2, cp_config=config)
    cp.pack()
    root_2.mainloop()
