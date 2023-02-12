from tkinter import *

import PIL.Image
import os
from imageforwidget import ImageForTkinter

letters_path = os.path.join(os.getcwd(), "../letters")
letters = {k: ImageForTkinter(fp=os.path.join(letters_path, k)) for k in os.listdir(letters_path)}


class TopFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(TopFrame, self).__init__(parent, *args, **kwargs)
        self.images_temp = {}
        self.image_label = Label(self, text="image...")
        self.image_label.pack()

    def load_image(self, fp):
        if fp in self.images_temp.keys():
            image = ImageForTkinter()
            image.image = self.images_temp.get(fp)
        else:
            image = ImageForTkinter(fp)
        image.resize(360, 360)
        self.images_temp[fp] = image.image
        lett:ImageForTkinter = letters.get("greenA.png")
        lett.resize(48,48)
        image.paste_image(lett.image)
        image.set_widget_image(self.image_label)


class PopUpWindow(Toplevel):
    def __init__(self):
        super(PopUpWindow, self).__init__()
        self.protocol("WM_DELETE_WINDOW", self.state("withdraw"))
        self.state("withdraw")


if __name__ == '__main__':
    import os

    dir_ = os.path.join(os.getcwd(), "../Python.png")
    root = Tk()
    img = TopFrame(root)
    img.pack()
    img.load_image(dir_)
    root.mainloop()
