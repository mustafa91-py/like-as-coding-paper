import datetime
from tkinter import *

TOOL_TIPS = {}


class ToolDict:
    pass


class ToolTip(Toplevel):
    def __init__(self):
        super(ToolTip, self).__init__()
        self.protocol("WM_DELETE_WINDOW", lambda: self.state("withdraw"))
        self.after_id = None
        self["bg"] = "yellow"
        self.current_widget: Label = None
        self.overrideredirect(1)
        self.widgets_information = {}
        self.wm_attributes("-alpha", 0)
        self.label = Label(self, bg=self["bg"])
        self.label.pack()
        self.groove()

    def resize_geometry_oto(self, add_x=70, add_y=None):
        x, y = self.winfo_pointerxy()
        _x, _y = self.winfo_width(), self.winfo_height()
        if _y + y > self.winfo_screenheight():
            r_pos_y = _y + y - self.winfo_screenheight()
        else:
            r_pos_y = 0
        if _x + x + 70 > self.winfo_screenwidth():
            r_pos_x = _x + x + 70 - self.winfo_screenwidth()
            r_pos_y += 30
        else:
            r_pos_x = 0
        if add_x:
            x += add_x
        if add_y:
            y += add_y
        self.geometry(f"+{x - r_pos_x}+{y - r_pos_y}")

    def update_widget(self, event):
        # self.state("normal")
        self.wm_attributes("-topmost", 1)
        self.wm_attributes("-alpha", .8)
        self.current_widget: Widget = event.widget
        w_x, w_y = self.current_widget.winfo_width(), self.current_widget.winfo_height()
        self.resize_geometry_oto(add_x=w_x, add_y=-w_y)
        self.label.configure(text=f"{self.widgets_information.get(event.widget)}")

    def groove(self):
        self.revolution()
        self.after_id = self.after(1000, self.groove)

    def message(self, widget, text):
        widget: Widget
        if widget not in self.widgets_information:
            widget.bind("<Enter>", self.update_widget, add="+")
            widget.bind("<Leave>", lambda e: self.wm_attributes('-alpha', 0), add="+")
        self.widgets_information[widget] = text

    def add_with_dict(self, data: dict):
        for widget, text in data.items():
            self.message(widget, text)

    def revolution(self):
        for widget, item in TOOL_TIPS.items():
            widget_ = sorted(item.items(), key=lambda x: int(x[0]))
            text_ = "\n".join([v for k, v in widget_])
            self.message(widget, text_)


if __name__ == '__main__':
    root = Tk()
    tool_tip = ToolTip()


    def goster(event):
        print(event.widget)
        TOOL_TIPS[b].update({2: str(datetime.datetime.now())})
        pass


    def add():
        TOOL_TIPS[b].update({2: str("basıldı")})


    b = Button(root, text="start", command=add)
    b.bind("<Enter>", goster)
    TOOL_TIPS[b] = {0: "button", 1: "göster"}
    b.pack()
    c = Label(root, text="ekle")
    c.pack()
    TOOL_TIPS[c] = {0: "ekle"}
    root.mainloop()
