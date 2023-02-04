from tkinter import *
from tkinter import font


class ScrollFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(ScrollFrame, self).__init__(parent, *args, **kwargs)
        # self.my_frame = Frame(self)
        self.canvasPaper = Canvas(self)
        self.child_frame = Frame(self.canvasPaper)
        self.__scroll_y = Scrollbar(self, orient="vertical", command=self.canvasPaper.yview)
        self.__scroll_y.pack(side="right", fill="y")
        self.__scroll_x = Scrollbar(self, orient="horizontal", command=self.canvasPaper.xview)
        self.__scroll_x.pack(side="bottom", fill="x")
        self.canvasPaper.configure(yscrollcommand=self.__scroll_y.set, xscrollcommand=self.__scroll_x.set)
        self.child_frame.bind("<Configure>",
                              lambda event: self.canvasPaper.configure(scrollregion=self.canvasPaper.bbox("all")))

        self.canvasPaper.create_window(0, 0, window=self.child_frame, anchor="nw")
        self.canvasPaper.pack(fill="y", expand=1)


class Units(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(Units, self).__init__(parent, *args, **kwargs)
        self.var = StringVar()
        self.__id = Label(self, text="None", name="id", font=font.Font(family="Times ", size=16))
        self.__cnf = dict(activebackground="green",
                          highlightbackground="red",
                          font=font.Font(family="Times", size=12),
                          padx=10,
                          command=self.high_light_button,
                          variable=self.var)

        self.a = Radiobutton(self, text="A", value="A", **self.__cnf)
        self.b = Radiobutton(self, text="B", value="B", **self.__cnf)
        self.c = Radiobutton(self, text="C", value="C", **self.__cnf)
        self.d = Radiobutton(self, text="D", value="D", **self.__cnf)
        self.e = Radiobutton(self, text="E", value="E", **self.__cnf)

        self.a.bind("<Button-3>", lambda event: self.deselect_(self.a))
        self.b.bind("<Button-3>", lambda event: self.deselect_(self.b))
        self.c.bind("<Button-3>", lambda event: self.deselect_(self.c))
        self.d.bind("<Button-3>", lambda event: self.deselect_(self.d))
        self.e.bind("<Button-3>", lambda event: self.deselect_(self.e))

        self.units = {"A": self.a, "B": self.b, "C": self.c, "D": self.d, "E": self.e}
        __pack = {"side": "left", "fill": "x", "expand": 1}
        self.__id.pack(**__pack)
        self.a.pack(**__pack)
        self.b.pack(**__pack)
        self.c.pack(**__pack)
        self.d.pack(**__pack)
        self.e.pack(**__pack)

    @property
    def id(self):
        return self.__id["text"]

    @id.setter
    def id(self, value):
        self.__id.configure(text=value)

    # @id.getter
    # def id(self):
    #     return self.__id["text"]

    def high_light_button(self):
        __select = self.var.get()
        for k, v in self.units.items():
            if __select == k:
                v.flash()
                v["bg"] = "gray"
            else:
                v["bg"] = "gray10"

    def __bind_deselect(self):
        for widget in self.units.values():
            widget.bind("<Button-3>", lambda event: self.deselect_(widget))

    def deselect_(self, widget):
        if widget["state"] == "normal" or widget["state"] == "active":
            widget.deselect()
            self.return_white()
            # self.groove()

    def return_white(self):
        if not self.var.get():
            for k, v in self.units.items():
                v["bg"] = "white"


class StackUnitsForAnswer(Toplevel):
    def __init__(self, amount: int, *args, **kwargs):
        super(StackUnitsForAnswer, self).__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", lambda: self.state("withdraw"))
        self.__scroll_frame = ScrollFrame(self)
        self.__scroll_frame.pack(fill="both", expand=1, anchor="nw")

        self.__amount = amount
        self.answer_fp = None
        self.title("answer key".title())
        self.units = {}
        self.create_stack()

    @property
    def amount(self):
        return self.__amount

    @amount.setter
    def amount(self, value):
        if isinstance(value, int):
            self.__amount = value
        else:
            raise ValueError(f"only type = int but you gave {type(value)}")

    def create_stack(self):
        for i in range(1, self.amount + 1):
            self.units[i] = Units(self.__scroll_frame.child_frame)
            self.units[i].id = str(i).zfill(3)
            self.units[i].pack()


class StackUnits(Frame):
    def __init__(self, parent, amount: int = 20, name: str = "test", *args, **kwargs):
        super(StackUnits, self).__init__(parent, *args, **kwargs)
        self.amount = amount
        self.name = name
        self.units = {}

        self.top_frame = LabelFrame(self)
        self.top_frame.pack(side="top", fill="x")

        self.test_name_label = Label(self.top_frame, text=f"{name}")
        self.test_name_label.pack(side="top", fill="x")

        self.__scroll_frame = ScrollFrame(self)
        self.__scroll_frame.pack(fill="both", expand=1, anchor="nw")

        self.bottom_frame = LabelFrame(self, text="bottom frame")
        self.bottom_frame.pack(side="bottom", fill="x")

        self.answer_top_level = StackUnitsForAnswer(amount)
        self.answer_top_level.amount = self.amount
        self.answer_keys_open_button = Button(self.bottom_frame, text="answer key",
                                              command=self.open_answers_top_level)
        self.answer_keys_open_button.pack()


    def create_stack(self):
        for i in range(1, self.amount + 1):
            self.units[i] = Units(self.__scroll_frame.child_frame)
            self.units[i].id = str(i).zfill(3)
            self.units[i].pack()

    def open_answers_top_level(self):
        self.answer_top_level.state("normal")
        self.answer_top_level.title(f"answer key = {self.name}")


if __name__ == '__main__':
    root = Tk()
    s_units = StackUnits(root, amount=30)
    s_units.create_stack()
    s_units.pack(fill="y", expand=1)
    root.mainloop()
