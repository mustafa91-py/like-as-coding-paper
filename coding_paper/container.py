import random
from dataclasses import dataclass, field, asdict
import os


@dataclass
class Container:
    file_path: os.path.abspath = None
    paper_key: dict = None
    answer_key: dict = None
    cp_config: dict = None
    amount: int = None
    name: str = None
    title: str = None
    after_id: object = None

    def result(self):
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
