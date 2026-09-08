from functools import cache

from nd_robotic_ai.robot.robot import LidarScanRangesTraceKind
from nd_robotic_ai.robot.robot import GaussianedQuaternionKinematic
from nd_robotic_ai.robot.robot import RosMultiModalYamlMessages


class Kinds:
    @cache
    def get_kind_list(self):
        kind_list = []
        # add the Finite classification
        kind_list.append(LidarScanRangesTraceKind())
        kind_list.append(GaussianedQuaternionKinematic())
        kind_list.append(RosMultiModalYamlMessages())

        return kind_list