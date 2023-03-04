import os.path
from tkinter import *
from tkinter import font
from features.screen_shot import ScreenShot
import folder_operations as fop
from pop_up_window.pop_up_window import PopUpWindow
from features.my_op_tooltip import TOOL_TIPS
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
        self.childFrame = Frame(self.canvasPaper)
        self.__scroll_y = Scrollbar(self, orient="vertical", command=self.canvasPaper.yview)
        self.__scroll_y.pack(side="right", fill="y")
        self.__scroll_x = Scrollbar(self, orient="horizontal", command=self.canvasPaper.xview)
        self.__scroll_x.pack(side="bottom", fill="x")
        self.canvasPaper.configure(yscrollcommand=self.__scroll_y.set, xscrollcommand=self.__scroll_x.set)
        self.childFrame.bind("<Configure>",
                             lambda event: self.canvasPaper.configure(scrollregion=self.canvasPaper.bbox("all")))

        self.canvasPaper.create_window(0, 0, window=self.childFrame, anchor="nw")
        self.canvasPaper.pack(fill="y", expand=1)


class Units(Frame):
    @log
    def __init__(self, parent, file_path, pop_up_window=None, container: dict = None, *args, **kwargs):
        """
                       self.__id  self.a self.b  self.c  self.d  self.e


                      ||        ||      ||      ||      ||     ||


        for e.x =    001        A       B       C       D      E   = class <Units>(1) overview

        :param parent:parent
        :param file_path: any folder path
        :param pop_up_window:class PopUpWindow
        :param container:class Container or any like that dataclass
        :param args:args for Frame
        :param kwargs:kwargs for Frame
        """
        super(Units, self).__init__(parent, *args, **kwargs)
        self.file_path = file_path
        self.container: Container = container
        self.popUpWindow: PopUpWindow = pop_up_window
        self.var = StringVar()  # common variable of widgets
        self.iid = self.__id = Label(self, text="None", name="id", font=font.Font(family="Times ", size=16))
        TOOL_TIPS[self.__id] = dict()
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

    def activate_is_exist_file_image_bind(self):
        self.__id.bind("<Enter>", self.check_out_image)

    def activate_pop_up_window(self):
        self.__id.bind("<Double-Button-1>", self.pop_up_top_level)

    def activate_ss_shot(self):
        self.__id.bind("<Button-3>", self.ss_shot)
        TOOL_TIPS[self.__id].update({0: "<right click> (get screen shot)"})

    @property
    def id(self):
        return self.__id["text"]

    @id.setter
    def id(self, value):
        self.__id.configure(text=value)

    def state_all(self, state_=DISABLED):
        widget: Radiobutton
        for widget in self.units.values():
            widget.configure(state=state_)

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

    def clear_stain(self) -> None:
        """
        the color of each marked unit(a,b,c,d,e,id) changes to white
        :return: None
        """
        for k, v in self.units.items():
            v["bg"] = "white"
            self.__id.configure(bg="white")

    @log
    def revamp_folder(self) -> os.path.abspath:
        """
        checks if the folder exists or not.
        If it does not exist, it creates a folder where images will be saved.
        :return: file_path
        """
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
    def check_out_image(self, event) -> None:
        """
        checks if there is a saved screenshot
        :param event: event
        :return: None
        """
        if not self.file_path:  # no file path is exit the function
            return
        widget = event.widget  # get widget
        file = os.path.join(self.revamp_folder(), f"id_{widget['text']}.png")  # location to checking screenshot
        if os.path.exists(file):  # if there is image the cursor changes
            widget.config(cursor="hand2")

            click = "double mouse left click"
            if all(self.container.answer_key.values()):
                TOOL_TIPS[self.__id].update({1: f"<{click}> open it ({widget['text']})"})
            else:
                TOOL_TIPS[self.__id].update({1: f"image = {widget['text']}"})

        else:
            widget.config(cursor="")
            TOOL_TIPS[self.__id].update({1: "image None"})

    @log
    def ss_shot(self, event) -> None:
        """
        take screenshot
        :param event: event
        :return: None
        """
        if not self.file_path:  # no file path is exit the function
            return
        widget = event.widget["text"]  # gets the widget's number

        ss = ScreenShot()  # screenshot class
        ss.ss_name = os.path.join(self.revamp_folder(), f"id_{widget}.png")  # location to save screenshot and name

        if self.popUpWindow.imageFrame.images_temp.get(ss.ss_name, None):
            # if a new image will be added on the same id, remove it from memory
            self.popUpWindow.imageFrame.images_temp.pop(ss.ss_name)

    @log
    def pop_up_top_level(self, event):
        if self.revamp_folder() is None:
            return
        widget = event.widget
        iid = widget["text"]  # iid get text

        __path = os.path.join(self.revamp_folder(), f"id_{iid}.png")
        if os.path.exists(__path):  # is exists path?
            # self.popUpWindow.iid_update(str(int(self.id)))  # id specifying which image(unit) will be uploaded
            self.popUpWindow.iid_update(iid)
            self.popUpWindow.imageFrame.ready_image(__path)

            self.popUpWindow.state("normal")
            self.popUpWindow.wm_attributes("-topmost", 1)
            self.popUpWindow.control = False


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
        self.wm_attributes("-topmost", 1)
        self.file_path = file_path
        self.units = {}  # storing the created class
        self.amount = amount  # number of units class or number of questions

        self.__scroll_frame = ScrollFrame(self)
        self.__scroll_frame.pack(fill="both", expand=1, anchor="nw")

        self.title("answer key".title())

        self.bottomFrame = LabelFrame(self, text="answer")
        self.bottomFrame.pack(side="bottom", fill="x")

        self.saveButton = Button(self.bottomFrame, text="save")
        self.saveButton.pack(side="bottom", fill="x")

        self.create_stack()
        self.topMenu = Menu(self)
        self.topMenu.add_command(label="reorganize", command=lambda: self.status_all(state_="normal"))
        self.configure(menu=self.topMenu)

    @log
    def create_stack(self) -> None:
        """
        created Units stack
        :return: None
        """
        for i in range(1, self.amount + 1):
            i = str(i).zfill(3)
            self.units[i] = Units(self.__scroll_frame.childFrame, self.file_path)
            self.units[i].id = i
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
        self.bottomFrame.configure(text=_text)

    def status_all(self, state_=DISABLED):
        unit: Units
        for unit in self.units.values():
            unit.state_all(state_=state_)


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
                 container: Container = None, *args,
                 **kwargs):
        super(StackUnits, self).__init__(parent, *args, **kwargs)
        self.amount = amount
        self.container = container
        self.popUpWindow = pop_up_window
        self.file_path = file_path
        self.lesson = title
        self.units = {}
        self.topFrame = LabelFrame(self)
        self.topFrame.pack(side="top", fill="x")

        self.testNameLabel = Label(self.topFrame, text=f"{title}")
        self.testNameLabel.pack(side="top", fill="x")

        self.__scroll_frame = ScrollFrame(self)
        self.__scroll_frame.pack(fill="both", expand=1, anchor="nw")

        self.bottomFrame = LabelFrame(self, text="bottom frame")
        self.bottomFrame.pack(side="bottom", fill="x")

        self.answerTopLevel = StackUnitsForAnswer(amount, self.file_path)
        self.answerTopLevel.amount = self.amount
        self.answerKeysOpenButton = Button(self.bottomFrame, text="answer key",
                                           command=self.open_answers_top_level)
        self.answerKeysOpenButton.pack(fill="x")

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
        self.bottomFrame.configure(text=_text)

    def groove(self) -> None:
        """
        constantly updated method for tkinter after
        :return: None
        """
        self.answerTopLevel.groove()
        self.elapsed_units()

    @log
    def create_stack(self) -> None:
        """
        created Units stack
        :return: None
        """
        for i in range(1, self.amount + 1):
            i = str(i).zfill(3)
            self.units[i] = Units(self.__scroll_frame.childFrame, self.file_path,
                                  pop_up_window=self.popUpWindow, container=self.container)
            self.units[i].id = i
            self.units[i].pack()
            self.units[i].activate_is_exist_file_image_bind()

    @log
    def open_answers_top_level(self) -> None:
        """
        pop up answer toplevel
        :return:
        """
        self.answerTopLevel.state("normal")
        self.answerTopLevel.title(f"answer key = {self.lesson}")

    def status_all(self, state_=DISABLED):
        unit: Units
        for unit in self.units.values():
            unit.state_all(state_=state_)

    def activate_pop_up_window(self):
        unit: Units
        for unit in self.units.values():
            unit.activate_pop_up_window()

    def activate_ss_shot(self):
        unit: Units
        for unit in self.units.values():
            unit.activate_ss_shot()


if __name__ == '__main__':
    from features.my_op_tooltip import ToolTip

    root = Tk()

    toolTips = ToolTip()
    s_units = StackUnits(root, amount=30)
    s_units.create_stack()
    s_units.pack(fill="y", expand=1)
    s_units.groove()
    toolTips.add_with_dict(TOOL_TIPS)
    root.mainloop()
