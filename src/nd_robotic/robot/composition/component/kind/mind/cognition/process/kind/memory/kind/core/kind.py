from nd_robotic.mind.cognition.process.kind.memory.kind.core.kinds_old import Kinds


class Kind:
    def __init__(self, kind:Kinds):
        if not isinstance(kind, Kinds):
            raise TypeError(f"kind must be an instance of Kinds, not {type(kind).__name__}")
        self._kind = kind

    def get_kind(self)->Kinds:
        return self._kind