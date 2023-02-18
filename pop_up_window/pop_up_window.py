from tkinter import *
from tkinter import font
import os
from container import Container
import folder_operations
from wtext import HighLightText

if __name__ == '__main__':
    from imageforwidget import ImageForTkinter
else:
    from .imageforwidget import ImageForTkinter

letters_path = os.path.join(os.getcwd(), "../letters")
letters = {k: ImageForTkinter(fp=os.path.join(letters_path, k)) for k in os.listdir(letters_path)}


class ImageFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super(ImageFrame, self).__init__(parent, *args, **kwargs)
        self["text"] = type(self).__name__
        self.images_temp = {}
        self.current_id = None
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


class PointFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super(PointFrame, self).__init__(parent, *args, **kwargs)
        self["text"] = type(self).__name__
        self.__container: Container = {}
        self.point_label_2_w = dict()
        self.point_var2 = IntVar()
        self.current_id = None

        for i in range(1, 11):
            self.point_label_2_w[i] = Label(self, text=i, font=font.Font(size=32), cursor="hand2")
            self.point_label_2_w[i].pack(side="left")
            self.point_label_2_w[i].bind("<Button-1>", self.star_icon)
            self.point_label_2_w[i].bind("<Button-3>", self.clear_point)
        # self.description = ScrolledText(self.f3, width=50, height=5)
        # self.description.grid(row=1, column=0)

    @property
    def container(self):
        return self.__container

    @container.setter
    def container(self, value):
        self.__container = value

    def star_icon(self, event):
        if event is not None:
            self.point_var2.set(int(event.widget["text"]))
        else:
            pass
        __img: ImageForTkinter = letters.get("star.png")
        img_gray: ImageForTkinter = letters.get("star2.png")
        for id_, kkk in self.point_label_2_w.items():
            if int(id_) <= self.point_var2.get():
                __img.set_widget_image(kkk)
            else:
                img_gray.set_widget_image(kkk)  # kkk.image = img_gray
        if cid := self.current_id:
            self.container.ids[cid]["point"] = self.point_var2.get()

    def one_time(self):
        if cid := self.container.ids.get(self.current_id):
            if point := cid.get("point", None):
                self.point_var2.set(point)
                self.star_icon(None)

    def clear_point(self, event):
        self.point_var2.set(0)
        img_gray: ImageForTkinter = letters.get("star2.png")
        for id_, kkk in self.point_label_2_w.items():
            img_gray.set_widget_image(kkk)

    def groove(self, **kwargs):
        """
        id değişsede point aynı kalıyor düzeltilecek
        id değişince alınan veriler hemen işlenmeli
        :param kwargs:
        :return:
        """
        self.container = kwargs.get("container")


class DescriptionFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super(DescriptionFrame, self).__init__(parent, *args, **kwargs)
        self["text"] = type(self).__name__
        self.container = None
        self.text = HighLightText(self, width=40, height=5)
        self.text.pack()

    def groove(self, **kwargs):
        self.container = kwargs.get("container")

    def one_time(self):
        pass


class PopUpWindow(Toplevel):
    def __init__(self, *args, **kwargs):
        super(PopUpWindow, self).__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", lambda: self.state("withdraw"))
        self.state("withdraw")
        self.current_id = None
        self.imageFrame = ImageFrame(self)
        self.imageFrame.pack()
        self.point = PointFrame(self)
        self.point.pack()
        self.description = DescriptionFrame(self)
        self.description.pack()
        self.control = False

    def groove(self, **kwargs):
        self.current_id = self.point.current_id = self.imageFrame.current_id
        self.point.groove(**kwargs)
        self.one_time_load_control(self.point.one_time)

    def one_time_load_control(self, *args):
        if self.control:
            return
        for arg in args:
            arg()
        self.control = True


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
