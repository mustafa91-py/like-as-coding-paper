import os.path

from units.units import StackUnits
from tkinter import *
from misc.save_dict import SaveDict


class CodingPaper(Frame):
    def __init__(self, parent, cp_config: dict = None, *args, **kwargs):
        super(CodingPaper, self).__init__(parent, *args, **kwargs)
        self.after_id = None
        self.coding_paper_keys = {}
        self.answer_keys = {}
        self.cp_config = cp_config
        self.amount = cp_config.get("amount")
        self.name = cp_config.get("name")
        self.file_path = cp_config.get("fp")

        self.save_dict = SaveDict(path_=self.file_path)

        self.stack_units = StackUnits(self, self.amount, self.name)
        self.stack_units.pack(fill="both", expand=1)
        self.stack_units.create_stack()
        self.groove()

    def groove(self):
        self.stack_units.groove()
        self.create_kwargs_for_save_dict()
        self.after_id = self.after(1000, self.groove)

    def get_data_to_stack_units(self):
        data_ = {k: v.var.get() for k, v in self.stack_units.units.items()}
        return data_

    def create_kwargs_for_save_dict(self):
        self.save_dict.space.update(self.cp_config)
        self.save_dict.space["paper_key"] = self.get_data_to_stack_units()


if __name__ == '__main__':
    root = Tk()
    # part input------------------------------------------------------
    title = "math_test_1"
    fp = os.path.join(os.getcwd(), "../garbage", f"{title}.json")
    cp_confg = dict(amount=28, name="physic".upper(), fp=fp, title=title)
    # part input------------------------------------------------------

    coding_paper = CodingPaper(root, cp_config=cp_confg)
    coding_paper.pack(fill="both", expand=1)
    root.mainloop()
