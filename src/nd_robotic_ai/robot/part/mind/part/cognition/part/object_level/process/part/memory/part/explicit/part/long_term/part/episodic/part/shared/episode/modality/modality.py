from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.perception.trace.group.group import \
    Group as TraceGroup
from nd_utility.data.kind.dic.dic import Dic


class Modality(TraceGroup):
    """
    Modality is one branch of a dic with its sequential data. time should not be considered  as an independent modality. Either the order of data represents the time or the time lable
    """
    def __init__(self, dic:Dic):
        TraceGroup.__init__(self, dic)