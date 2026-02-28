from nd_robotic.mind.cognition.process.kind.perception.state.state import State
from nd_physics.dimension.unit import Scalar

class TimedState(State):
    def __init__(self, time:Scalar):
        self._time = time

    def get_time(self)->Scalar:
        return self._time