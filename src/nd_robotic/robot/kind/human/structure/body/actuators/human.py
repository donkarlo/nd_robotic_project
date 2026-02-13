from typing import List, Optional

from nd_robotic.robot.robot import Mind
from nd_robotic.robot.robot import Actuator
from nd_robotic.robot.robot import Robot
from nd_robotic.robot.robot import Group


class Human(Robot):
    """
    This class represts real human and teh actions or messages it can generate
    - a human can convey a message. the robot may or maynot obay
    """
    def __init__(self, actuators: List[Actuator], sensor_collection: Group, mind: Mind, name: Optional[str] = None):
        pass