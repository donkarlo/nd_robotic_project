from typing import Any

from nd_robotic.robot.robot import Component


class SendMessage(Component):
    def __init__(self, message:Any):
        self._message = message