from nd_robotic.robot.state.state import State


class Homeostasis(State):
    def __init__(self):
        self._rate = 100

    def get_rate(self) -> float:
        return self._rate
