import folder_operations
from coding_paper.coding_paper import CodingPaper, asdict
from input_window.input_frame import InputFrame
from tkinter import *
import folder_operations as fop
import os

if __name__ == '__main__':
    root_2 = Tk()
    from features.my_op_tooltip import ToolTip

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
