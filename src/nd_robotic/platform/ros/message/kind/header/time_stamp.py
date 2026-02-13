from nd_physics.quantity.kind.time.time import Time
from nd_robotic.platform.ros.message.field.field import Field
from nd_robotic.platform.ros.message.message import Message

from nd_utility.data.kind.dic.dic import Dic
class TimeStamp(Message):
    def __init__(self, seconds:int, nano_seconds:int):
        self._second = seconds
        self._nano_second = nano_seconds
        super().__init__([Field("seconds", self._second), Field("nano_seconds", self._nano_second)])
        self._time = Time(self._second + self._nano_second/ 1e9)

    @classmethod
    def init_from_dic(cls, dic: Dic) -> "TimeStamp":
        stamp = dic["header"]["stamp"]
        second = stamp["secs"]
        nano_second = stamp["nsecs"]
        return cls(second, nano_second)

    def get_time(self)->Time:
        return self._time
