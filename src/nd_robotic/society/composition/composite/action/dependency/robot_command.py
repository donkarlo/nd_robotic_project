from nd_robotic.spa.action.action import Action
from nd_robotic.robot.robot import Robot


class RobotAction:
    def __init__(self, robot:Robot, action:Action):
        self._robot = robot
        self._action = action