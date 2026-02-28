from nd_robotic.robot.robot import Kind as GroupTraceKind
from functools import cache
from nd_robotic.robot.robot import LidarScanRanges as LidarScanRangesTraceKind

from nd_utility.data.kind.dic.dic import Dic


class LidarScanRanges(GroupTraceKind):
    """
    """

    def __init__(self):
        self._trace_kind: TraceKind = LidarScanRangesTraceKind()
        super().__init__(self._trace_kind.get_name())
    @cache
    def get_schema(self) -> Dic:
        return self._trace_kind.get_schema()


