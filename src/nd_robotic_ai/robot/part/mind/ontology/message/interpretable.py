from nd_robotic_ai.robot.robot import Robot
from typing import Protocol, Any

class interpretable(Protocol):
    def get_interpretion(self, interpreter:Robot)->Any: ...
