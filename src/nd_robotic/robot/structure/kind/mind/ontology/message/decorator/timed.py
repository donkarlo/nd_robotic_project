from nd_physics.dimension.unit.scalar import Scalar
from nd_robotic.robot.robot import Interface

class Timed(Decorator):
    def __init__(self, inner:Interface, time:Scalar):
        self._time = time
        super().__init__(inner)
    def get_time(self)->Time:
        return self._time