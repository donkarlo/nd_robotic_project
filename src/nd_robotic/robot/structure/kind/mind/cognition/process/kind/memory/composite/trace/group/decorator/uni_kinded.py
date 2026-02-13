
from nd_robotic.robot.robot import Interface as TraceGroupInterface
from nd_robotic.robot.robot import Kind as TraceGroupKind


class UniKinded(Decorator):
    def __init__(self, inner: TraceGroupInterface, kind: TraceGroupKind):
        super().__init__(inner)
        self._kind = kind

    def get_kind(self) -> TraceGroupKind:
        return self._kind