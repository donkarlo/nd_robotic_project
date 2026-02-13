from nd_robotic.robot.robot import Component
from nd_physics.kinematics.pose import Pose


class TakePose(Component):
    def __init__(self, pose: Pose) -> None:
        self._pos = pose

    def run(self) -> None:
        pass