import datetime


class MyDateTime(datetime.datetime):
    def __init__(self, *args, **kwargs):
        super().__init__()

    @classmethod
    def to_dict(cls):
        now = cls.now()
        year, month, day = now.year, now.month, now.day
        hour, minute, second = now.hour, now.minute, now.second
        _dict = dict(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        return _dict


if __name__ == '__main__':
    d = MyDateTime.to_dict()
    print(d)