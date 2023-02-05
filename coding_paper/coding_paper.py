import os.path

from units.units import StackUnits
from tkinter import *
from misc.save_dict import SaveDict
from container import Container, asdict


class CodingPaper(Frame):
    def __init__(self, parent, cp_config: dict = None, *args, **kwargs):
        super(CodingPaper, self).__init__(parent, *args, **kwargs)
        self.container = Container(**cp_config)

        self.after_id = None
        self.save_dict = SaveDict(path_=self.container.file_path)

        self.stack_units = StackUnits(self, self.container.amount, self.container.lesson)
        self.stack_units.pack(fill="both", expand=1)
        self.stack_units.create_stack()
        self.groove()

    def groove(self):
        self.container.paper_key = self.get_data_to_stack_units()
        self.container.answer_key = self.get_data_to_answer_stack_units()
        self.stack_units.groove()
        self.after_id = self.after(250, self.groove)

    def get_data_to_stack_units(self):
        data_ = {k: v.var.get() for k, v in self.stack_units.units.items()}
        return data_

    def get_data_to_answer_stack_units(self):
        data_ = {k: v.var.get() for k, v in self.stack_units.answer_top_level.units.items()}
        return data_


if __name__ == '__main__':
    garbage_ = os.path.join(os.getcwd(), "../garbage")
    if not os.path.exists(garbage_):
        os.mkdir(garbage_)

    root = Tk()

    title = "lokman"

    # part input------------------------------------------------------
    fp = os.path.join(os.getcwd(), "../garbage", f"{title}.json")
    cp_confg = dict(lesson="physic".upper(), file_path=fp, title=title)
    # part input------------------------------------------------------
    coding_paper = CodingPaper(root, cp_config=cp_confg)

    coding_paper.pack(fill="both", expand=1)


    def save_exit():
        coding_paper.save_dict.space = asdict(coding_paper.container)
        coding_paper.save_dict.save()
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", save_exit)
    root.mainloop()
