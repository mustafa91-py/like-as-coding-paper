import random
from dataclasses import dataclass, field, asdict
import os


@dataclass
class Container:
    file_path: os.path.abspath = None
    paper_key: dict = None
    answer_key: dict = None
    amount: int = field(default=20)  # number of questions
    unit_time: int | float = field(default=1)  # time per unit(question)
    lesson: str = field(default="math")  # lesson
    subject: str = field(default="integral")  # subject
    title: str = field(default="test1")  # title

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


if __name__ == '__main__':
    c = Container()
    c.amount = 20
    ttt = "ABCDE "
    c.answer_key = {k: random.choice("ABCDE") for k, v in enumerate(range(5))}
    c.paper_key = {k: random.choice(ttt) for k, v in enumerate(range(5))}
    print(c.result())
    print(asdict(c))