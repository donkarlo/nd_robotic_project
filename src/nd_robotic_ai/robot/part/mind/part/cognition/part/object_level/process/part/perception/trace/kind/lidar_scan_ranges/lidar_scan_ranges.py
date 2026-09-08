from nd_math.linear_algebra.tensor.vector.vector import Vector
from functools import cache

from nd_utility.data.kind.dic.dic import Dic


class LidarScanRanges:
    """
    """

    def __init__(self):
        super().__init__("lidar_scan_ranges")
    @cache
    def get_schema(self) -> Dic:
        trace_kind_schema = \
            {
                "ranges": Vector
            }


