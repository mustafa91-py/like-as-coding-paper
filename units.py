from tkinter import *
from tkinter import font


class Units(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(Units, self).__init__(parent, *args, **kwargs)
        self.var = StringVar()
        self.id = Label(self, text="None", name="id", font=font.Font(family="Times ", size=16))
        self.__cnf = {"activebackground": "green",
                      "highlightbackground": "red",
                      "font": font.Font(family="Times ", size=12),
                      "padx": 10}
        self.A = Radiobutton(self, text="A", variable=self.var, value="A", command=self.high_light_button, **self.__cnf)
        self.B = Radiobutton(self, text="B", variable=self.var, value="B", command=self.high_light_button, **self.__cnf)
        self.C = Radiobutton(self, text="C", variable=self.var, value="C", command=self.high_light_button, **self.__cnf)
        self.D = Radiobutton(self, text="D", variable=self.var, value="D", command=self.high_light_button, **self.__cnf)
        self.E = Radiobutton(self, text="E", variable=self.var, value="E", command=self.high_light_button, **self.__cnf)
        self.units = {"A": self.A, "B": self.B, "C": self.C, "D": self.D, "E": self.E}
        __pack = {"side": "left", "fill": "x", "expand": 1}
        self.id.pack(**__pack)
        self.A.pack(**__pack)
        self.B.pack(**__pack)
        self.C.pack(**__pack)
        self.D.pack(**__pack)
        self.E.pack(**__pack)

    def high_light_button(self):
        __select = self.var.get()
        for k, v in self.units.items():
            if __select == k:
                v.flash()
                v["bg"] = "gray"
            else:
                v["bg"] = "gray10"


if __name__ == '__main__':
    root = Tk()
    units = Units(root)
    units.pack()
    root.mainloop()
