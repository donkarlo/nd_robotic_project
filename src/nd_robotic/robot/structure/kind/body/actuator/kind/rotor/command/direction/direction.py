from nd_robotic.robot.robot import Command
from nd_robotic.robot.robot import Status


class Direction(Command):
    def __init__(self, status:Status):
        self._status = status
        super().__init__()