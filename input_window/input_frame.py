from tkinter import *


class TopFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super(TopFrame, self).__init__(parent, *args, **kwargs)
        self.lesson = Label(self, text="lesson")
        self.subject = Label(self, text="subject")
        self.title = Label(self, text="title")
        self.lesson.grid(row=0, column=0)
        self.subject.grid(row=1, column=0)
        self.title.grid(row=2, column=0)

        self.lesson_entry_var = StringVar()
        self.lesson_entry = Entry(self, textvariable=self.lesson_entry_var)

        self.subject_entry_var = StringVar()
        self.subject_entry = Entry(self, textvariable=self.subject_entry_var)

        self.title_entry_var = StringVar()
        self.title_entry = Entry(self, textvariable=self.title_entry_var)

        self.lesson_entry.grid(row=0, column=1)
        self.subject_entry.grid(row=1, column=1)
        self.title_entry.grid(row=2, column=1)

    def out_put(self):
        out = dict(lesson=self.lesson_entry_var.get(),
                   subject=self.subject_entry_var.get(),
                   title=self.title_entry_var.get())
        return out


class MidFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super(MidFrame, self).__init__(parent, *args, **kwargs)
        self.amount = Label(self, text="amount")
        self.unit_per_minute = Label(self, text="unit per min")
        self.unit_per_minute.bind("<Button-1>", self.switch_time)
        self.value_on_off = 1

        self.amount.grid(row=0, column=0)
        self.unit_per_minute.grid(row=1, column=0)
        self.amount_var = DoubleVar()
        self.amount_scale = Scale(self, variable=self.amount_var,
                                  to=20, from_=1,
                                  resolution=1,
                                  orient=HORIZONTAL,
                                  length=250, command=self.try_command)
        self.amount_scale.grid(row=0, column=1)
        self.amount_scale.set(10)
        self.unit_per_minute_var = DoubleVar()
        self.total_time_var = DoubleVar()
        self.unit_per_minute_scale = Scale(self, from_=.1, to=10, variable=self.unit_per_minute_var,
                                           resolution=.1, orient=HORIZONTAL, length=200,)
        self.unit_per_minute_scale.grid(row=1, column=1)
        self.unit_per_minute_scale.set(1)

    def switch_time(self, event):
        label_: Label = event.widget

        if self.value_on_off % 2 == 0:
            self.set_unit_time()
            label_.configure(text="unit per min")
        else:
            self.set_total_time()
            label_.configure(text="total time(min)")
            self.configure(text=f"unit per min = {self.total_time_var.get():.2f})")
        self.value_on_off += 1
        self["text"] = "..."

    def set_total_time(self):
        self.unit_per_minute_scale.configure(from_=1, to=500, resolution=1)
        self.unit_per_minute_scale.configure(command=self.get_total_time)

    def get_total_time(self, value=None):
        _ = float(self.unit_per_minute_var.get() / self.amount_var.get())
        self.total_time_var.set(_)
        self.configure(text=f"unit per min = {_:.2f})")
        return _

    def set_unit_time(self):
        self.unit_per_minute_scale.configure(from_=.1, to=10, resolution=.1)
        # self.unit_per_minute_scale.set(1)
        self.unit_per_minute_scale.configure(command=lambda v: self.configure(
            text=f"unit per min = {self.unit_per_minute_var.get():.1f})"))

    def try_command(self, value):
        current_to = self.amount_scale["to"]
        length_ = self.amount_scale["length"]
        if self.value_on_off % 2 == 0:
            self.get_total_time()
        if current_to >= 250:
            return
        percent = round((int(value) / float(current_to) * 100), 2)
        if percent >= 90:
            self.amount_scale.configure(to=current_to + 5, length=length_ + 10)
            self.amount_scale.set(value)
        self.unit_per_minute_scale.configure(length=self.amount_scale["length"])

    def out_puts(self):
        out = dict(amount=self.amount_scale.get(),
                   unit_time=self.unit_per_minute_scale.get())
        if self.value_on_off % 2 == 0:
            out["unit_time"] = self.total_time_var.get()
        else:
            out["unit_time"] = self.unit_per_minute_var.get()
        return out


class InputFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(InputFrame, self).__init__(parent, *args, **kwargs)
        self.topFrame = TopFrame(self)
        self.topFrame.pack()
        self.midFrame = MidFrame(self)
        self.midFrame.pack()
        self.out_kw = {}
        self.create_paper = Button(self, text="create", command=self.take_kwargs)
        self.create_paper.pack()

    def take_kwargs(self):
        kwargs = {}
        kwargs.update(self.topFrame.out_put())
        kwargs.update(self.midFrame.out_puts())
        self.out_kw.update(kwargs)
        self.pack_forget()


if __name__ == '__main__':
    root = Tk()
    inputf = InputFrame(root)
    inputf.pack()
    root.mainloop()
