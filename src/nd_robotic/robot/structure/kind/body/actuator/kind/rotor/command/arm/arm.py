from nd_robotic.robot.robot import Command
from nd_robotic.robot.robot import Status


class Arm(Command):
    def __init__(self, status: Status):
        self._status = status
        super().__init__()

    def get_status(self) -> Status:
        return self._status