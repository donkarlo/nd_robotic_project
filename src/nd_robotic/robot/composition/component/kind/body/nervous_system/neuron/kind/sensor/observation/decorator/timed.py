from nd_robotic.robot.robot import Interface
from nd_robotic.robot.robot import Decorator
from nd_physics.dimension.unit.scalar import Scalar


class Timed(Decorator):
    def __init__(self, inner:Interface, time:Scalar):
        self._time:Scallar = time
        super().__init__(inner)

    def get_time(self):
        return self._time

    def get_time_val(self):
        return self._time.get_val()