from nd_robotic.robot.robot import Kind as GroupTraceKind
from nd_utility.data.kind.dic.dic import Dic
from nd_utility.oop.inheritance.overriding.override_from import override_from


class RosMultiModalYamlMessages(GroupTraceKind):
    def __init__(self):
        super().__init__("RosMultiModalYamlMessages")

    @override_from(GroupTraceKind)
    def get_schema(self) ->Dic:
        schema = Dic({})
        return schema