import os.path

import folder_operations
from units.units import StackUnits
from tkinter import *
from tkinter.messagebox import showwarning
from misc.save_dict import SaveDict
from pop_up_window.pop_up_window import PopUpWindow

from container import Container, asdict


class TimeLine(LabelFrame):
    def __init__(self, parent, container: Container, *args, **kwargs):
        super(TimeLine, self).__init__(parent, *args, **kwargs)
        self.after_id = None
        self.container = container
        self.timer = self.container.amount * (self.container.unit_time * 60)
        self.label = Label(self)
        self.label.pack(fill="x")
        self.start_button = Button(self, text="start exam", command=self.start_timer)
        self.start_button.pack(fill="x")
        self.label.configure(text=self.convert_time_format())

    def groove(self):
        self.label.configure(text=self.convert_time_format())
        self.timer -= 1
        self.after_id = self.after(1000, self.groove)

    def convert_time_format(self):
        if self.timer < 0:
            return
        minute, second = divmod(self.timer, 60)
        if minute < 60:
            return f"{str(minute).zfill(2)} min, {str(second).zfill(2)} sec"
        else:
            hour, minute = divmod(minute, 60)
            return f"{str(hour).zfill(2)} hour ,{str(minute).zfill(2)} min, {str(second).zfill(2)} sec"

    def start_timer(self):
        self.start_button.configure(state="disabled")
        self.start_button.pack_forget()
        self.groove()


class ResultFrame(LabelFrame):
    def __init__(self, parent, container: Container, *args, **kwargs):
        super(ResultFrame, self).__init__(parent, *args, **kwargs)
        self.container = container
        self.finish_button = Button(self, text="finish")
        self.finish_button.pack(fill="x")


class CodingPaper(Frame):
    def __init__(self, parent, cp_config: dict = None, *args, **kwargs):
        super(CodingPaper, self).__init__(parent, *args, **kwargs)
        self.after_id = None
        self.topFrame = Frame(self)
        self.middleFrame = Frame(self)
        self.bottomFrame = Frame(self)

        self.topFrame.pack(fill="x")
        self.middleFrame.pack(fill="x")
        self.bottomFrame.pack(fill="x")

        if cp_config.get("amount", 0) > 250:
            cp_config["amount"] = 250
            showwarning("max value fixed oto", f"amount = 250 ,maximum value of 250 can be given")

        self.container = Container(**cp_config)
        self.container.create_ids()
        self.file_path = self.container.file_path

        self.popUpWindow = PopUpWindow(container=self.container)
        self.save_dict = SaveDict(path_=cp_config.get("file_path"))

        self.stack_units = StackUnits(self.middleFrame, self.container.amount,
                                      file_path=self.file_path,
                                      title=self.container.lesson,
                                      pop_up_window=self.popUpWindow, container=self.container)
        self.stack_units.pack(fill="both", expand=1)
        self.stack_units.create_stack()
        self.stack_units.answer_keys_open_button.configure(state="disabled")
        self.timeLine = TimeLine(self.topFrame, container=self.container, text="timer")
        self.timeLine.pack(fill="x")
        self.timeLine.start_button.configure(command=self.start)
        self.resultFrame = ResultFrame(self.bottomFrame, container=self.container, text="resultFrame")
        self.resultFrame.finish_button.configure(command=self.finish)

        self.groove()
        self.stack_units.status_all()

    def groove(self):
        self.container.paper_key = self.get_data_to_stack_units()
        self.container.answer_key = self.get_data_to_answer_stack_units()
        self.stack_units.groove()
        self.popUpWindow.groove()
        self.timeline_is_zero()
        self.after_id = self.after(250, self.groove)

    def get_data_to_stack_units(self):
        data_ = {str(k): v.var.get() for k, v in self.stack_units.units.items()}
        return data_

    def get_data_to_answer_stack_units(self):
        data_ = {str(k): v.var.get() for k, v in self.stack_units.answer_top_level.units.items()}
        return data_

    def stain(self):
        from units.units import Units
        if all(self.container.answer_key.values()):
            for paper, answer in zip(self.stack_units.units.items(), self.stack_units.answer_top_level.units.items()):
                # i_p, i_a = paper[0], answer[0]
                w_p: Units = paper[1]
                w_a: Units = answer[1]
                widget = w_p.units.get(w_p.var.get())
                correct_widget = w_p.units.get(w_a.var.get())
                if w_p.var.get() == w_a.var.get():
                    widget.configure(bg="green")
                    w_p.iid.configure(bg="green")
                elif w_p.var.get() == "":
                    correct_widget.configure(bg="lightgreen")
                    w_p.iid.configure(bg="gray")
                else:
                    widget.configure(bg="red")
                    correct_widget.configure(bg="lightgreen")
                    w_p.iid.configure(bg="red")
                for radiobutton_p, radiobutton_a in zip(w_p.units.values(), w_a.units.values()):
                    radiobutton_p.configure(state="disabled")
                    radiobutton_a.configure(state="disabled")

    def start(self):
        self.timeLine.start_timer()
        self.stack_units.status_all("normal")
        self.resultFrame.pack(fill="x")

    def finish(self):
        self.stack_units.answer_keys_open_button.configure(state="normal")
        self.timeLine.after_cancel(self.timeLine.after_id)
        self.stack_units.status_all()
        self.stack_units.activate_ss_shot()

    def timeline_is_zero(self):
        if self.timeLine.timer < 0:
            self.stack_units.status_all()
            self.stack_units.activate_ss_shot()
            self.timeLine.after_cancel(self.timeLine.after_id)


class CodingPaperOpen(Frame):
    def __init__(self, parent, file_path, *args, **kwargs):
        super(CodingPaperOpen, self).__init__(parent, *args, **kwargs)
        # Frame.__init__(self, parent, *args, **kwargs)
        self.file_path = file_path
        self.save_dict = SaveDict(path_=self.file_path)
        assert self.save_dict.space.get("file_path") is not None, f"file reading error\n{file_path=}"
        self.container = Container(**self.save_dict.space)
        self.popUpWindow = PopUpWindow(container=self.container)
        self.container.create_ids()
        __ = {k: v for k, v in self.save_dict.space.items() if k in ["amount", "title"]}
        self.stack_units = StackUnits(self, file_path=self.file_path,
                                      pop_up_window=self.popUpWindow, container=self.container,
                                      **__)
        self.stack_units.pack(fill="both", expand=1)
        self.stack_units.save_id = self.container.file_path
        self.stack_units.create_stack()

        self.load()
        self.groove()
        self.stack_units.activate_pop_up_window()
        self.stack_units.activate_ss_shot()

    def groove(self, **kwargs):
        self.popUpWindow.groove()
        print(self.save_dict.space)
        self.save_dict.space = asdict(self.container)
        self.after(250, self.groove)

    def load(self):
        for iid, uni in self.stack_units.units.items():
            uni.var.set(self.container.paper_key.get(str(iid)))
        for iid, uni in self.stack_units.answer_top_level.units.items():
            uni.var.set(self.container.answer_key.get(str(iid)))
        self.stain()

    def stain(self):
        from units.units import Units
        if all(self.container.answer_key.values()):
            for paper, answer in zip(self.stack_units.units.items(), self.stack_units.answer_top_level.units.items()):
                # i_p, i_a = paper[0], answer[0]
                w_p: Units = paper[1]
                w_a: Units = answer[1]
                widget = w_p.units.get(w_p.var.get())
                correct_widget = w_p.units.get(w_a.var.get())
                if w_p.var.get() == w_a.var.get():
                    widget.configure(bg="green")
                    w_p.iid.configure(bg="green")
                elif w_p.var.get() == "":
                    correct_widget.configure(bg="lightgreen")
                    w_p.iid.configure(bg="gray")
                else:
                    widget.configure(bg="red")
                    correct_widget.configure(bg="lightgreen")
                    w_p.iid.configure(bg="red")
            self.stack_units.status_all()
            self.stack_units.answer_top_level.status_all()


if __name__ == '__main__':
    garbage_ = os.path.join(os.getcwd(), "../garbage")
    if not os.path.exists(garbage_):
        os.mkdir(garbage_)

    root = Tk()

    title = "test"

    # part input------------------------------------------------------
    fp = os.path.join(folder_operations.FOLDER_PATH, f"{title}.json")
    cp_confg = dict(lesson="physic".upper(), file_path=fp, amount=6, title=title)
    # part input------------------------------------------------------
    coding_paper = CodingPaper(root, cp_config=cp_confg)

    coding_paper.pack(fill="both", expand=1)


    def save_exit():
        coding_paper.save_dict.space = asdict(coding_paper.container)
        coding_paper.save_dict.save()
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", save_exit)
    root.mainloop()
