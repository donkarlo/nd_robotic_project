from nd_robotic.platform.ros.message.kind.header.frame_id_stack import FrameIdStack
from nd_robotic.platform.ros.message.kind.header.time_stamp import TimeStamp
from nd_utility.data.kind.dic.dic import Dic

class Header:
    def __init__(self, time_stamp: TimeStamp, frame_id_stack:FrameIdStack,sequence:int):
        self._time_stamp = time_stamp
        self._frame_id_stack = frame_id_stack
        self._sequence = sequence

    def get_time_stamp(self)->TimeStamp:
        return self._time_stamp

    def get_frame_sequence(self)->FrameIdStack:
        return self._frame_id_stack


    @classmethod
    def init_from_ros_message_dic(cls, dic:Dic)->"Header":
        time_stamp = TimeStamp.get_time_by_dic(dic)
        frame_id_stack = FrameIdStack.init_from_message_dic(dic)
        sequence = dic["header"]["seq"]
        return(cls(time_stamp, frame_id_stack, sequence))
