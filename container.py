import datetime
import random
from dataclasses import dataclass, field, asdict
import os
import folder_operations as fpo


@dataclass
class Container:
    file_path: os.path.abspath
    paper_key: dict = None
    answer_key: dict = None
    amount: int = field(default=20)  # number of questions
    unit_time: float = field(default=1)  # time per unit(question)
    lesson: str = field(default="math")  # lesson
    subject: str = field(default="integral")  # subject
    title: str = field(default="test1")  # title
    ids: dict = None
    log_datetime: dict = None
    elapsed_time: int = None
    source: str = None

    def result(self) -> dict:
        if self.paper_key is not None and self.answer_key is not None:
            data_ = zip(self.paper_key.items(), self.answer_key.items())
            out_put = {}
            for k, v in data_:
                if k[1] in list("ABCDE"):
                    if k == v:
                        out_put[k[0]] = True
                    else:
                        out_put[k[0]] = False
                else:
                    out_put[k[0]] = None
            return out_put

    def create_ids(self):
        if not isinstance(self.ids, dict):
            self.ids = dict()
            for i in range(1, self.amount + 1):
                self.ids[str(i).zfill(3)] = {k: None for k in ["image", "solved", "point", "desc"]}

    def get_data(self):
        self.create_ids()
        ss_file_dir = os.path.join(fpo.SS_SHOT, self.oto_file_name())
        if not os.path.exists(ss_file_dir):
            return
        images = os.listdir(os.path.join(ss_file_dir))
        images = [os.path.abspath(os.path.join(fpo.SS_SHOT, self.oto_file_name(), p)) for p in images]
        if images:
            for img in images:
                iid = os.path.split(img)[-1]
                iid = os.path.splitext(iid)[0]
                iid = str(iid.split("_")[-1])
                iid = str(int(iid))
                if isinstance(self.ids.get(iid, None), dict):
                    self.ids[iid]["images"] = img

    def oto_file_name(self):
        fm = f"{self.lesson}_{self.subject}_{self.title}"
        return fm


if __name__ == '__main__':
    c = Container(file_path=None)
    c.amount = 20
    ttt = "ABCDE "
    c.answer_key = {k: random.choice("ABCDE") for k, v in enumerate(range(5))}
    c.paper_key = {k: random.choice(ttt) for k, v in enumerate(range(5))}
    print(c.result())
    print(asdict(c))
