from tkinter import *

import PIL.Image

from imageforwidget import ImageForTkinter


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
        image.set_widget_image(self.image_label)
        self.images_temp[fp] = image.image
        print(self.images_temp)
        print(type(image.image))
        print(isinstance(image.image,PIL.Image.Image))
        image2 = ImageForTkinter.load(self.images_temp.get(fp))
        # image2.image = self.images_temp.get(fp)
        image2.resize(500,500)
        image2.set_widget_image(self.image_label)
        print(image2.image)


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
