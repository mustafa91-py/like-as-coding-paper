import datetime
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
letters_path = folder_operations.letters_path
letters = {k: ImageForTkinter(fp=os.path.join(letters_path, k)) for k in os.listdir(letters_path)}


class RepoImage:
    letters = {}

    def preloading_letter(self, fp=None):
        if fp is None:
            letters_dir = folder_operations.letters_path
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


class ImageFrame(LabelFrame, RepoImage):
    def __init__(self, parent, container: Container, *args, **kwargs):
        super(ImageFrame, self).__init__(parent, *args, **kwargs)
        self["text"] = type(self).__name__
        self.navigatorFrame = LabelFrame(self)
        self.navigatorFrame.pack(side="top", fill="x", expand=1)
        self.fake_labels = dict()
        self.fake_labels_fp = dict()
        self.images_temp = {}
        self.current_id = None
        self.container = container
        self.image_label = Label(self, text="image...")
        self.image_label.pack()
        self.sx, self.sy = 360, 360
        self.preloading_letter()
        self.pre_loading_images()

    def groove(self, **kwargs):
        # self.container = kwargs.get("container")
        pass

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

    def get_images_in_folder(self) -> list | None:
        """
        eğer resimler var ise ön yükleme seçeneği eklenecek ...
        :return:List or None
        """
        file = self.container.file_path
        if os.path.exists(file):
            directory, file_ = os.path.split(file)
            name_, ext = os.path.splitext(file_)
            sshot_path = os.path.join(folder_operations.SS_SHOT, name_)
            if os.path.exists(sshot_path):
                ss: str
                get_tree_png = [os.path.join(sshot_path, ss) for ss in os.listdir(sshot_path)
                                if ss.startswith("id") and ss.endswith(".png")]
                return get_tree_png
            else:
                return None
        else:
            return None

    def pre_loading_images(self) -> None:
        if images := self.get_images_in_folder():
            for image_path in images:
                image = ImageForTkinter(image_path)
                self.images_temp[image_path] = image.image

    def create_navigator_labels(self):
        for img_path, image in self.images_temp.items():
            file: str = os.path.split(img_path)[1]
            file: str = os.path.splitext(file)[0]
            iid = file.split("_")[1]
            iid = str(iid).zfill(3)
            if iid not in self.fake_labels:
                self.fake_labels_fp[iid] = img_path
                self.fake_labels[iid] = Label(self.navigatorFrame, text=iid)

        for label in sorted(self.fake_labels.values(), key=lambda x: int(x["text"])):
            label: Label
            label.pack_forget()
            label.pack(side="left", fill="x", expand=1)

    def bind_add_fake_labels(self, func):
        label: Label
        for label in self.fake_labels.values():
            label.bind("<Button-1>", func)

    def load_image(self, fp):
        if fp in self.images_temp.keys():
            image = ImageForTkinter.load(self.images_temp.get(fp))
        else:
            image = ImageForTkinter(fp)
        image.resize(self.sx, self.sy)
        self.images_temp[os.path.abspath(fp)] = image.image  # image added image_temp dict
        image.set_widget_image(self.image_label)

        return image

    def ready_image(self, __path):
        new = self.load_image(__path)
        __answer = self.container.answer_key
        __paper = self.container.paper_key
        __answer = __answer.get(str(int(self.current_id)))
        __paper = __paper.get(str(int(self.current_id)))
        if __answer == __paper:
            color = f"green{__paper}"
        elif __paper == "":
            color = f"None"
        else:
            color = f"red{__paper}"
        letters_images = self.letters
        new.paste_image(letters_images.get(f"green{__answer}"))
        new.paste_image(letters_images.get(color), side="se")
        new.set_widget_image(self.image_label)
        self.create_navigator_labels()


class PointFrame(LabelFrame, RepoImage):
    def __init__(self, parent, container: Container, *args, **kwargs):
        super(PointFrame, self).__init__(parent, *args, **kwargs)
        self["text"] = type(self).__name__
        self.__container = container

        self.statusFrame = LabelFrame(self)
        self.pointFrame = LabelFrame(self)

        self.statusFrame.pack(side="left")
        self.pointFrame.pack(fill="x", side="left")

        self.statusCheckButtonVar = IntVar()
        self.statusCheckButton = Checkbutton(self.statusFrame, onvalue=1, offvalue=0)
        self.statusCheckButton.pack(side="bottom")
        self.statusImageLabel = Label(self.statusFrame, text="image...")
        self.statusImageLabel.pack()

        self.point_label_2_w = dict()
        self.point_var2 = IntVar()
        self.current_id = None

        for i in range(1, 11):
            self.point_label_2_w[i] = Label(self.pointFrame, text=i, font=font.Font(size=32), cursor="hand2")
            self.point_label_2_w[i].pack(side="left")
            self.point_label_2_w[i].bind("<Button-1>", self.star_icon)
            self.point_label_2_w[i].bind("<Button-3>", self.clear_point)
        self.star_icon(None)
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
            else:
                self.point_var2.set(0)
                self.star_icon(None)

    def clear_point(self, event):
        self.point_var2.set(0)
        img_gray: ImageForTkinter = letters.get("star2.png")
        for id_, kkk in self.point_label_2_w.items():
            img_gray.set_widget_image(kkk)

    def groove(self, **kwargs):
        # self.container = kwargs.get("container")
        pass


class DescriptionFrame(LabelFrame):
    def __init__(self, parent, container: Container, *args, **kwargs):
        super(DescriptionFrame, self).__init__(parent, *args, **kwargs)
        self["text"] = type(self).__name__
        self.container = container
        self.current_id = None
        self.text = HighLightText(self, width=40, height=5)
        self.text.pack()
        # self.text.bind("<Enter>", self.update_text)
        self.text.bind("<Leave>", self.update_text)

    def groove(self, **kwargs):
        # self.container = kwargs.get("container")
        pass

    def one_time(self):
        if cid := self.container.ids.get(self.current_id):
            if desc := cid.get("desc", None):
                self.text.delete(0.0, "end")
                desc = str(desc).replace("\n\n\n", "")
                self.text.insert(0.0, desc)
            else:
                self.text.delete(0.0, "end")
                self.text.insert(0.0, f"created {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    def update_text(self, event):
        widget: HighLightText = event.widget
        assert self.container is not None, f"{self.container=} is not must be empty"
        try:
            if cid := self.container.ids.get(self.current_id):
                cid["desc"] = widget.get(0.0, "end")
        except AttributeError as _:
            self["text"] = f"{_=}"
            self.configure(bg="red")
            widget.delete(0.0, "end")
            widget.configure(bg="black", fg="red")
            error_message = f"you may have call forgotten\n{Container.create_ids=} "
            widget.insert(0.0, error_message)
            return
        self["text"] = f"{self.__class__.__name__} saved {datetime.datetime.now()}"


class PopUpWindow(Toplevel):
    def __init__(self, container: Container, *args, **kwargs):
        super(PopUpWindow, self).__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", lambda: self.state("withdraw"))
        self.state("withdraw")
        self.container = container
        self.current_id = None
        self.imageFrame = ImageFrame(self, self.container)
        self.imageFrame.pack()
        self.point = PointFrame(self, self.container)
        self.point.pack()
        self.description = DescriptionFrame(self, self.container)
        self.description.pack()
        self.control = False

    def groove(self, **kwargs):
        self.imageFrame.groove(**kwargs)
        self.point.groove(**kwargs)
        self.description.groove(**kwargs)
        self.one_time_load_control(self.point.one_time,
                                   self.description.one_time)

        self.imageFrame.bind_add_fake_labels(self.open_image_with_fake_label)

    def iid_update(self, iid):
        self.point.current_id = self.imageFrame.current_id = self.description.current_id = self.current_id = iid

    def one_time_load_control(self, *args):
        if self.control:
            return
        for arg in args:
            arg()
        self.control = True

    def open_image_with_fake_label(self, event):
        widget = event.widget
        iid = widget["text"]
        self.iid_update(str(int(iid)))
        self.imageFrame.ready_image(self.imageFrame.fake_labels_fp.get(iid))
        self.control = False


if __name__ == '__main__':
    import os

    root = Tk()
    c = Container("test")
    c.create_ids()
    pop = PopUpWindow(c)
    pop.title("test".title())
    pop.state("normal")
    img = pop.imageFrame
    img.preloading_letter()
    # print(img.letters)
    next_ = Button(root, text="popUpToplevel", command=lambda: pop.state("normal"))
    next_.pack()
    root.mainloop()
