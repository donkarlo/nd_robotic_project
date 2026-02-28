from nd_physics.quantity.kind.time.time import Time
from nd_robotic.robot.robot import Decorator
from nd_robotic.robot.robot import Interface as TraceInterface


class Timed(Decorator):
    def __init__(self, inner: TraceInterface, time:Time):
        Decorator.__init__(self, inner)
        self._time = time
    def get_time(self)->Time:
        return self._time
