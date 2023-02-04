from tkinter import *
from tkinter import font


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
        for i in [self.a, self.b, self.c, self.d, self.e]:
            i.bind("<Button-3>", lambda event: self.deselect_(i))

    def deselect_(self, widget):
        if widget["state"] == "normal" or widget["state"] == "active":
            widget.deselect()
            self.return_white()
            # self.groove()

    def return_white(self):
        if not self.var.get():
            for k, v in self.units.items():
                v["bg"] = "white"


if __name__ == '__main__':
    root = Tk()
    units = Units(root)
    units.id = str(1).zfill(3)
    units.pack()
    root.mainloop()
