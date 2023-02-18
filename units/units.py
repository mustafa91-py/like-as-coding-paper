import os.path
from tkinter import *
from tkinter import font
from features.screen_shot import ScreenShot
import folder_operations as fop
from pop_up_window.pop_up_window import PopUpWindow
from container import Container
import datetime


def log(func):
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        # print(func, datetime.datetime.now())

        return f

    return wrapper


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
    @log
    def __init__(self, parent, file_path, pop_up_window=None, container: dict = None, *args, **kwargs):
        """
                   self.__id  self.a self.b  self.c  self.d  self.e
                      ||        ||      ||      ||      ||     ||
        for e.x =    001        A       B       C       D      E   = class <Units>(1) overview

        :param parent:
        :param args:
        :param kwargs:
        """
        super(Units, self).__init__(parent, *args, **kwargs)
        self.file_path = file_path
        self.container: Container = container
        self.popUpWindow: PopUpWindow = pop_up_window
        self.var = StringVar()  # common variable of widgets
        self.iid = self.__id = Label(self, text="None", name="id", font=font.Font(family="Times ", size=16))
        self.__id.bind("<Enter>", self.is_exists_image_file)
        # number(id) of widgets
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
        # self.iid.bind("<Button-1>", lambda e: print(self.revamp_folder(), e.widget))
        self.__id.bind("<Button-3>", self.ss_shot)
        self.__id.bind("<Double-Button-1>", self.pop_up_top_level)

    @property
    def id(self):
        return self.__id["text"]

    @id.setter
    def id(self, value):
        self.__id.configure(text=value)

    @log
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

    @log
    def deselect_(self, widget) -> None:
        """
        if widget is not selected
        :param widget: radiobutton | widget
        :return: None
        """
        if widget["state"] == "normal" or widget["state"] == "active":
            widget.deselect()
            self.return_white()

    @log
    def return_white(self) -> None:
        """
        if the selection is removed
        :return: None
        """
        if not self.var.get():
            for k, v in self.units.items():
                v["bg"] = "white"

    @log
    def revamp_folder(self):
        if not self.file_path:
            return
        split = os.path.split(self.file_path)
        f = split[0]
        name = os.path.splitext(split[1])
        will_create = os.path.join(fop.SS_SHOT, name[0])
        if not os.path.exists(will_create):
            os.mkdir(will_create)
        return will_create

    @log
    def is_exists_image_file(self, event):
        if not self.file_path:
            return
        widget = event.widget
        file = os.path.join(self.revamp_folder(), f"id_{widget['text']}.png")
        if os.path.exists(file):
            widget.config(cursor="hand2")
        else:
            widget.config(cursor="")

    @log
    def ss_shot(self, event):
        # print(self.file_path)
        if not self.file_path:
            return
        # print(type(self).__name__, self.file_path, )
        widget = event.widget["text"]
        ss = ScreenShot()
        ss.ss_name = os.path.join(self.revamp_folder(), f"id_{widget}.png")
        if self.popUpWindow.imageFrame.images_temp.get(ss.ss_name, None):
            self.popUpWindow.imageFrame.images_temp.pop(ss.ss_name)

    @log
    def pop_up_top_level(self, event):
        if self.revamp_folder() is None:
            return
        widget = event.widget
        iid = widget["text"]

        # print(f"{self.file_path=},{self.revamp_folder()=}")
        # print(f"{widget=},{iid=}")
        __path = os.path.join(self.revamp_folder(), f"id_{iid}.png")
        if os.path.exists(__path):
            new = self.popUpWindow.imageFrame.load_image(__path)
            __answer = self.container.answer_key
            __paper = self.container.paper_key
            __answer = __answer.get(str(int(self.id)))
            __paper = __paper.get(str(int(self.id)))
            self.popUpWindow.imageFrame.current_id = str(int(self.id))
            if __answer == __paper:
                color = f"green{__paper}"
            elif __paper == "":
                color = f"None"
            else:
                color = f"red{__paper}"
            letters_images = self.popUpWindow.imageFrame.letters
            new.paste_image(letters_images.get(f"green{__answer}"))
            new.paste_image(letters_images.get(color), side="se")
            new.set_widget_image(self.popUpWindow.imageFrame.image_label)
            self.popUpWindow.state("normal")
            self.popUpWindow.wm_attributes("-topmost", 1)
            self.popUpWindow.current_id = str(int(self.id))
            self.popUpWindow.point.control = False

class StackUnitsForAnswer(Toplevel):
    """
                       self.__id  self.a self.b  self.c  self.d  self.e
                      ||        ||      ||      ||      ||     ||
        for e.x =    001        A       B       C       D      E   = class <Units>(1) overview
                     002        A       B       C       D      E   = class <Units>(2) overview
                     .          .       .       .       .      .        .
                     .          .       .       .       .      .        .

    """

    def __init__(self, amount: int, file_path, *args, **kwargs):
        super(StackUnitsForAnswer, self).__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", lambda: self.state("withdraw"))
        self.state("withdraw")
        self.file_path = file_path
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

    @log
    def create_stack(self) -> None:
        """
        created Units stack
        :return: None
        """
        for i in range(1, self.amount + 1):
            self.units[i] = Units(self.__scroll_frame.child_frame, self.file_path)
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

    @log
    def __init__(self, parent, amount: int = None, file_path=None, title: str = "test", pop_up_window=None,
                 container: dict = None, *args,
                 **kwargs):
        super(StackUnits, self).__init__(parent, *args, **kwargs)
        self.amount = amount
        self.container = container
        self.popUpWindow = pop_up_window
        self.file_path = file_path
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

        self.answer_top_level = StackUnitsForAnswer(amount, self.file_path)
        self.answer_top_level.amount = self.amount
        self.answer_keys_open_button = Button(self.bottom_frame, text="answer key",
                                              command=self.open_answers_top_level)
        self.answer_keys_open_button.pack()

    # @log
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

    @log
    def create_stack(self) -> None:
        """
        created Units stack
        :return: None
        """
        for i in range(1, self.amount + 1):
            self.units[i] = Units(self.__scroll_frame.child_frame, self.file_path,
                                  pop_up_window=self.popUpWindow, container=self.container)
            self.units[i].id = str(i).zfill(3)
            self.units[i].pack()

    @log
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
