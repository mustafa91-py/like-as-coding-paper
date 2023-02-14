import os.path
from tkinter import *

import PIL.Image
from PIL import ImageTk, Image


class ImageForTkinter:
    def __init__(self, fp=None):
        if isinstance(fp, PIL.Image.Image):
            self.image = fp
        else:
            self.image: Image.open = Image.open(fp=fp)

        # self.wild_image = self.image.copy()
        self.second_image = None
        self.widget_ = None

    def resize(self, w, h):
        self.image = self.image.resize((w, h))

    @classmethod
    def load(cls, image):
        return cls(fp=image)

    def set_widget_image(self, widget: Widget = None):
        img = ImageTk.PhotoImage(self.image)
        self.widget_ = widget
        if widget is not None:
            widget = widget
        else:
            if isinstance(widget, Widget):
                widget = self.widget_
            else:
                return None
        widget.configure(image=img)
        widget.image = img
        print(self.widget_)

    def paste_image(self, fp=None, size=None, side="ne"):
        if isinstance(fp, PIL.Image.Image):
            self.second_image = fp
        else:
            self.second_image = Image.open(fp)

        if size is not None:
            self.second_image = self.second_image.copy().resize(size)
        posx = self.image.size[0] - self.second_image.size[0]
        posy = self.image.size[1] - self.second_image.size[1]
        if side == "ne":
            self.image.paste(self.second_image, (posx, 0))
        elif side == "se":
            self.image.paste(self.second_image, (posx, posy))
        self.set_widget_image()
        return type(self).load(self.image)


if __name__ == "__main__":
    root = Tk()
    state = {0: "wait.png", 1: "done.png"}
    dir_ = os.path.join(os.getcwd(), "../Python.png")
    img = ImageForTkinter(dir_)
    a = Label(root, text="a")
    img.resize(400, 350)
    img.paste_image(os.path.join("../letters", "greenA.png"), size=(64, 64), side="ne")
    img.paste_image(os.path.join("../letters", "grayB.png"), size=(64, 64), side="se")
    img.set_widget_image(a)

    a.pack()
    root.mainloop()
