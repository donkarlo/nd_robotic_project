from nd_robotic.robot.robot import Robot


class Prototype:
    def __init__(self, name: str, sample:Robot):
        self._name = name
    def get_name(self) -> str:
        return self._name