import os.path
from tkinter import *
from tkinter import font
from features.screen_shot import ScreenShot


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
        """
                   self.__id  self.a self.b  self.c  self.d  self.e
                      ||        ||      ||      ||      ||     ||
        for e.x =    001        A       B       C       D      E   = class <Units>(1) overview
                     002        A       B       C       D      E   = class <Units>(2) overview
                     .          .       .       .       .      .        .
                     .          .       .       .       .      .        .

        :param parent:
        :param args:
        :param kwargs:
        """
        super(Units, self).__init__(parent, *args, **kwargs)
        self.var = StringVar()  # common variable of widgets
        self.iid = self.__id = Label(self, text="None", name="id", font=font.Font(family="Times ", size=16))
        # number(id) of widgets
        self.save_id = None
        self.__cnf = dict(activebackground="green",
                          highlightbackground="red",
                          font=font.Font(family="Times", size=12),
                          padx=10,
                          command=self.high_light_button,
                          variable=self.var)
        # widgets config dict

        self.__pack = {"side": "left", "fill": "x", "expand": 1}
        # widgets pack config dict

        self.a = Radiobutton(self, text="A", value="A", **self.__cnf)
        self.b = Radiobutton(self, text="B", value="B", **self.__cnf)
        self.c = Radiobutton(self, text="C", value="C", **self.__cnf)
        self.d = Radiobutton(self, text="D", value="D", **self.__cnf)
        self.e = Radiobutton(self, text="E", value="E", **self.__cnf)
        # widgets are created

        self.units = {"A": self.a, "B": self.b, "C": self.c, "D": self.d, "E": self.e}
        # dictionary of widgets

        self.__id.pack(**self.__pack)
        for __rb in self.units.values():
            __rb.bind("<Button-3>", lambda event: self.deselect_(event.widget))
            __rb.pack(**self.__pack)
        # widgets bind func and packed
        self.iid.bind("<Button-1>", lambda e: print(e.widget))
        self.iid.bind("<Button-3>", self.ss_shot)

    @property
    def id(self):
        return self.__id["text"]

    @id.setter
    def id(self, value):
        self.__id.configure(text=value)

    def high_light_button(self) -> None:
        """
        if widget is selected , colors to be given (flash)
        :return: None
        """
        __select = self.var.get()
        for k, v in self.units.items():
            if __select == k:
                v.flash()
                v["bg"] = "gray"
            else:
                v["bg"] = "gray10"

    def deselect_(self, widget) -> None:
        """
        if widget is not selected
        :param widget: radiobutton | widget
        :return: None
        """
        if widget["state"] == "normal" or widget["state"] == "active":
            widget.deselect()
            self.return_white()

    def return_white(self) -> None:
        """
        if the selection is removed
        :return: None
        """
        if not self.var.get():
            for k, v in self.units.items():
                v["bg"] = "white"

    def ss_shot(self, event):
        # if self.save_id:
        widget = event.widget["text"]
        ss = ScreenShot()
        ss.ss_name = os.path.join(os.getcwd(), "../garbage", f"id_{widget}.png")


class StackUnitsForAnswer(Toplevel):
    """
                       self.__id  self.a self.b  self.c  self.d  self.e
                      ||        ||      ||      ||      ||     ||
        for e.x =    001        A       B       C       D      E   = class <Units>(1) overview
                     002        A       B       C       D      E   = class <Units>(2) overview
                     .          .       .       .       .      .        .
                     .          .       .       .       .      .        .

    """

    def __init__(self, amount: int, *args, **kwargs):
        super(StackUnitsForAnswer, self).__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", lambda: self.state("withdraw"))
        self.state("withdraw")
        self.units = {}  # storing the created class
        self.amount = amount  # number of units class or number of questions

        self.__scroll_frame = ScrollFrame(self)
        self.__scroll_frame.pack(fill="both", expand=1, anchor="nw")

        self.title("answer key".title())

        self.bottom_frame = LabelFrame(self, text="answer")
        self.bottom_frame.pack(side="bottom", fill="x")

        self.save_button = Button(self.bottom_frame, text="save")
        self.save_button.pack(side="bottom", fill="x")

        self.create_stack()

    def create_stack(self) -> None:
        """
        created Units stack
        :return: None
        """
        for i in range(1, self.amount + 1):
            self.units[i] = Units(self.__scroll_frame.child_frame)
            self.units[i].id = str(i).zfill(3)
            self.units[i].pack()

    def groove(self) -> None:
        """
        constantly updated method for tkinter after
        :return: None
        """
        self.elapsed_units()

    def elapsed_units(self) -> None:
        """
        calculating percentage
        :return: None
        """
        v: Units
        tick = {k: v for k, v in self.units.items() if v.var.get()}
        tick = len(tick)
        percent_ = round((tick / self.amount) * 100, 2)
        _text = f"marked : {tick} unmarked : {self.amount - tick} ( % {percent_}) "
        self.bottom_frame.configure(text=_text)


class StackUnits(Frame):
    """
                       self.__id  self.a self.b  self.c  self.d  self.e
                      ||        ||      ||      ||      ||     ||
        for e.x =    001        A       B       C       D      E   = class <Units>(1) overview
                     002        A       B       C       D      E   = class <Units>(2) overview
                     .          .       .       .       .      .        .
                     .          .       .       .       .      .        .

    """

    def __init__(self, parent, amount: int = None, title: str = "test", *args, **kwargs):
        super(StackUnits, self).__init__(parent, *args, **kwargs)
        self.amount = amount
        self.lesson = title
        self.units = {}

        self.top_frame = LabelFrame(self)
        self.top_frame.pack(side="top", fill="x")

        self.test_name_label = Label(self.top_frame, text=f"{title}")
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

    def elapsed_units(self) -> None:
        """
        calculating percentage
        :return: None
        """

        v: Units
        tick = {k: v for k, v in self.units.items() if v.var.get()}
        tick = len(tick)
        percent_ = round((tick / self.amount) * 100, 2)
        _text = f"marked : {tick} unmarked : {self.amount - tick} ( % {percent_:^9} ) "
        self.bottom_frame.configure(text=_text)

    def groove(self) -> None:
        """
        constantly updated method for tkinter after
        :return: None
        """
        self.answer_top_level.groove()
        self.elapsed_units()

    def create_stack(self) -> None:
        """
        created Units stack
        :return: None
        """
        for i in range(1, self.amount + 1):
            self.units[i] = Units(self.__scroll_frame.child_frame)
            self.units[i].id = str(i).zfill(3)
            self.units[i].pack()

    def open_answers_top_level(self) -> None:
        """
        pop up answer toplevel
        :return:
        """
        self.answer_top_level.state("normal")
        self.answer_top_level.title(f"answer key = {self.lesson}")


if __name__ == '__main__':
    root = Tk()
    s_units = StackUnits(root, amount=30)
    s_units.create_stack()
    s_units.pack(fill="y", expand=1)
    s_units.groove()
    root.mainloop()
