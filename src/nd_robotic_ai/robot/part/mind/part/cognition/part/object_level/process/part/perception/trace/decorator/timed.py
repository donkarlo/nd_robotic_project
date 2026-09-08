from nd_physics.quantity.kind.time.time import Time
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.leaf.leaf import \
    Decorator

from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.leaf.leaf import \
    Interface as TraceInterface


class Timed(Decorator):
    def __init__(self, inner: TraceInterface, time: Time):
        Decorator.__init__(self, inner)
        self._time = time

    def get_time(self) -> Time:
        return self._time
