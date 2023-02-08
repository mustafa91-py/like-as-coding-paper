from coding_paper.coding_paper import CodingPaper,asdict
from input_window.input_window import Window, Stage
from tkinter import *
import folder_operations as fop
import os

if __name__ == '__main__':
    root = Window()
    root.mainloop()
    print(Stage.config)
    config: dict = Stage.config
    config["amount"] = 5
    config["file_read"] = False
    file_name = f"{config.get('lesson')}_{config.get('subject')}_{config.get('title')}"
    fp = os.path.join(fop.FOLDER_PATH,file_name)
    config["file_path"] = fp
    print(config)

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
