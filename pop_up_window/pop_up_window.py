from tkinter import *

import os

import folder_operations
if __name__ == '__main__':
    from imageforwidget import ImageForTkinter
else:
    from .imageforwidget import ImageForTkinter

letters_path = os.path.join(os.getcwd(), "../letters")
letters = {k: ImageForTkinter(fp=os.path.join(letters_path, k)) for k in os.listdir(letters_path)}


class ImageFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(ImageFrame, self).__init__(parent, *args, **kwargs)
        self.images_temp = {}
        self.letters = {}
        self.image_label = Label(self, text="image...")
        self.image_label.pack()
        self.sx, self.sy = 360, 360
        self.preloading_letter()

    def preloading_letter(self, fp=None):
        if fp is None:
            letters_dir = os.path.join(os.getcwd(), "../letters")
        else:
            letters_dir = fp
        if os.path.exists(letters_dir):
            abs_path = [os.path.abspath(os.path.join(letters_dir, p)) for p in os.listdir(letters_dir)]
            for path in abs_path:
                __img = ImageForTkinter(path)
                __img.resize(32, 32)
                __text = os.path.split(path)
                __text = os.path.splitext(__text[1])[0]
                self.letters[__text] = __img.image

    @property
    def width_x(self):
        return self.sx

    @width_x.setter
    def width_x(self, x):
        self.sx = x

    @property
    def height_y(self):
        return self.sy

    @height_y.setter
    def height_y(self, y):
        self.sy = y

    def top_right(self, ):
        pass

    def bottom_right(self, ):
        pass

    def load_image(self, fp):
        if fp in self.images_temp.keys():
            image = ImageForTkinter.load(self.images_temp.get(fp))
        else:
            image = ImageForTkinter(fp)
        image.resize(self.sx, self.sy)
        self.images_temp[os.path.abspath(fp)] = image.image
        image.set_widget_image(self.image_label)

        return image
        # lett: ImageForTkinter = letters.get("greenA.png")
        # lett.resize(48, 48)
        # image.paste_image(self.letters.get("grayA"))


class PopUpWindow(Toplevel):
    def __init__(self, *args, **kwargs):
        super(PopUpWindow, self).__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", lambda: self.state("withdraw"))
        self.state("withdraw")
        self.imageFrame = ImageFrame(self)
        self.imageFrame.pack()


if __name__ == '__main__':
    import os

    dir_ = os.path.join(folder_operations.SS_SHOT, "test", )
    list_ = [os.path.join(dir_, p) for p in os.listdir(dir_)]
    print(list_)
    dir_ = os.path.join(dir_, list_[0])
    k = 1


    def load():
        global k
        # print(list_[k % len(list_)] in img.images_temp)
        # print(list_[k % len(list_)])
        # img.load_image()
        a = img.load_image(list_[k % len(list_)]).paste_image(img.letters.get("grayB"))
        b = a.paste_image(img.letters.get("greenC"), side="se")
        b.set_widget_image(img.image_label)
        # print(img.images_temp)
        k += 1
        # root.after(10,load)


    root = Tk()
    pop = PopUpWindow(root)
    pop.state("normal")

    img = pop.imageFrame
    img.preloading_letter()
    print(img.letters)
    # img.width_x = 800
    # load()
    next_ = Button(root, text="next", command=load)
    next_.pack()
    root.mainloop()
