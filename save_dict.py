import os
import json


class SaveDict:
    def __init__(self, path_=None, oto=True):
        self.path_ = path_
        self.oto_create = oto
        self.dir, self.name = os.path.split(self.path_)
        if not os.path.exists(self.path_) and self.oto_create:
            open(self.path_, "w").close()
        self.space = dict()
        __load = self.load()
        self.space.update(__load)
        self.save()
        self.__up_keys()

    def save(self):
        with open(self.path_, "w", encoding="utf-8") as f:
            json.dump(self.space, f, ensure_ascii=False)

    def load(self) -> dict:
        with open(self.path_, "r", encoding="utf-8") as f:
            try:
                read = json.load(f)
                return read
            except json.decoder.JSONDecodeError:
                return {}

    def __up_keys(self):
        keys_ = {str(k).replace(" ", "_").lower(): v for k, v in self.space.items()}
        self.__dict__["keys"] = self.space.keys()
        self.__dict__.update(keys_)
