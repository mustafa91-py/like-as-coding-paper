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
    unit_time: int | float = field(default=1)  # time per unit(question)
    lesson: str = field(default="math")  # lesson
    subject: str = field(default="integral")  # subject
    title: str = field(default="test1")  # title
    ids: dict = None

    def result(self) -> dict:
        if self.paper_key is not None and self.answer_key is not None:
            data_ = zip(self.paper_key.items(), self.answer_key.items())
            out_put = {}
            for k, v in data_:
                if k[1] in "ABCDE":
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
                self.ids[i] = {k: None for k in ["image", "solved", "point", "desc"]}

    def get_data(self):
        self.create_ids()
        images = os.listdir(os.path.join(fpo.SS_SHOT, self.title))
        images = [os.path.abspath(os.path.join(fpo.SS_SHOT, self.title, p)) for p in images]
        if images:
            for img in images:
                iid = os.path.split(img)[-1]
                iid = os.path.splitext(iid)[0]
                iid = str(iid.split("_")[-1])
                iid = str(int(iid))
                self.ids[iid]["images"] = img


if __name__ == '__main__':
    c = Container(file_path=None)
    c.amount = 20
    ttt = "ABCDE "
    c.answer_key = {k: random.choice("ABCDE") for k, v in enumerate(range(5))}
    c.paper_key = {k: random.choice(ttt) for k, v in enumerate(range(5))}
    print(c.result())
    print(asdict(c))
