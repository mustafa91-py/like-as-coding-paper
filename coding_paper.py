from units import StackUnits
from tkinter import *


class CodingPaper(Frame):
    def __init__(self, parent, cp_config: dict = None, *args, **kwargs):
        super(CodingPaper, self).__init__(parent, *args, **kwargs)
        self.amount = cp_config.get("amount")
        self.name = cp_config.get("name")
        self.stack_units = StackUnits(self, self.amount, self.name)
        self.stack_units.pack(fill="both", expand=1)
        self.stack_units.create_stack()
        self.stack_units.groove()


if __name__ == '__main__':
    root = Tk()
    cp_config = dict(amount=28, name="hello")
    coding_paper = CodingPaper(root, cp_config=cp_config)
    coding_paper.pack(fill="both", expand=1)
    root.mainloop()
