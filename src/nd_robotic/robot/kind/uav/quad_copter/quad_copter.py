from typing import Optional

from nd_robotic.robot.robot import Group

from nd_robotic.robot.robot import Robot
from nd_robotic.robot.robot import Mind
from nd_robotic.robot.robot import RotorSet


class QuadCopter(Robot):
    def __init__(self, rotor_set:RotorSet, sensor_collection:Group, mind:Mind, name: Optional[str]=None):
        super().__init__(rotor_set, sensor_collection, mind, name)