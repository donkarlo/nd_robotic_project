from nd_robotic.robot.robot import Timed
from nd_robotic.robot.robot import LidarScanRanges
from nd_robotic.platform.ros.message.field.field import Field
from nd_robotic.platform.ros.message.message import Message
from nd_robotic.platform.ros.message.kind.header.time_stamp import TimeStamp
from nd_utility.data.kind.dic.dic import Dic
from nd_robotic.robot.robot import Observation as LidarObservation
from typing import List
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.trace.trace import Trace as Trace


class Scan(Message):
    def __init__(self, fields:List[Field]):
        super().__init__(fields)
        if self.get_field_value_by_name("ranges") is None or self.get_field_value_by_name("time") is None:
            raise ValueError("ranges must be between field.__name s")
        self._time = self.get_field_value_by_name("time")

    @classmethod
    def init_from_dic(cls, dic: Dic) -> "Scan":


        fields = []

        #time
        time = TimeStamp.init_from_dic(dic).get_time()
        field = Field("time", time)
        fields.append(field)

        ##
        value = dic["angle_min"]
        field = Field("angle_min", value)
        fields.append(field)

        ##
        value = dic["angle_max"]
        field = Field("angle_max", value)
        fields.append(field)

        ##
        value = dic["angle_increment"]
        field = Field("angle_increment", value)
        fields.append(field)

        ##
        value = dic["range_min"]
        field = Field("range_min", value)
        fields.append(field)

        ##
        value = dic["range_max"]
        field = Field("range_max", value)
        fields.append(field)

        ##
        value = dic["ranges"]
        field = Field("ranges", value)
        fields.append(field)

        ##
        value = dic["intensities"]
        field = Field("intensities", value)
        fields.append(field)

        return cls(fields)

    @staticmethod
    def is_this_message_type_from_dic(dic: Dic) -> bool:
        if not dic.has_nested_keys(["ranges"]):
            return False
        return True

    def get_scan_ranges_trace(self)-> Trace:
        trace = Trace.init_from_formatted_data_and_kind_and_name(LidarObservation(self.get_field_value_by_name("ranges")), LidarScanRanges() ,None)
        timed_trace = Timed(trace, self._time)
        return timed_trace
