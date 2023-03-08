from tkinter import *
import pyautogui
import mss
import mss.tools


class SelectScreenShot(Canvas):

    def __init__(self, parent, ss_name, *args, **kwargs):
        super(SelectScreenShot, self).__init__(parent, *args, **kwargs)
        self["cursor"] = "cross"
        self.bind("<Button-3>", self.screenshot)
        self.bind("<B1-Motion>", self.motion)
        self.top_x, self.top_y = None, None
        self.right_x, self.right_y = None, None
        self.ss_name = ss_name
        self.motion_data = list()
        self.bind("<Button-1>", lambda event: self.motion_data.clear())

    def motion(self, event):
        self.motion_data.append(pyautogui.position())
        self.top_x, self.top_y = self.motion_data[0]
        self.right_x, self.right_y = self.motion_data[-1]
        self.draw_rect()

    def draw_rect(self):
        self.delete("rect")
        bbox = (self.top_x, self.top_y, self.right_x, self.right_y)
        self.create_rectangle(bbox, tags=("rect",), width=4, fill="green", dash=(5, 250, 5), outline="red")

    def screenshot(self, event):
        self.master: Toplevel
        self.master.wm_attributes("-alpha", 0)
        print(self.ss_name)
        try:
            with mss.mss() as sct:
                monitor = {"top": self.top_y, "left": self.top_x,
                           "width": self.right_x - self.top_x, "height": self.right_y - self.top_y}
                sct_image = sct.grab(monitor)
                mss.tools.to_png(sct_image.rgb, sct_image.size, output=self.ss_name)
            self.delete("all")
        except TypeError:
            pass
        finally:
            self.master.destroy()


class ScreenShot(Toplevel):
    """
    1 - hold left mouse button and drag (select area)
    3 - save and exit right click (if rectangle is selected)
    2 - exit double Mouse left click

    """

    def __init__(self, *args, **kwargs):
        super(ScreenShot, self).__init__(*args, **kwargs)
        self.wm_attributes("-fullscreen", 1)
        self.wm_attributes("-topmost", 1)
        self.wm_attributes("-alpha", .3)
        self.wm_attributes("-transparentcolor", "green")
        self.__name = "uuu.png"
        self.bind("<Double-Button-1>", lambda event: self.back_destroy())
        self.screen_shot = SelectScreenShot(self, self.__name)
        self.screen_shot.pack(fill="both", expand=1)

    @property
    def ss_name(self):
        return self.__name

    @ss_name.setter
    def ss_name(self, value):
        self.__name = value
        self.screen_shot.ss_name = value

    def back_destroy(self):
        self.destroy()
        Process.SS_OPEN = False


if __name__ == '__main__':
    root = Tk()
    s = ScreenShot(root)
    s.ss_name = "garbage/test.png"
    Button(root, text="ss", command=lambda: s.state("normal")).pack()
    root.mainloop()
