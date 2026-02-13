from abc import ABC, abstractmethod

from nd_utility.data.kind.dic.dic import Dic
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.trace.kind.core.kind import Kind as  SingleTraceKind


class Kind(ABC):
    """
    Should represent a relation that relates a society of traces together. Such as Iranian in Human being
    """
    def __init__(self, name: str):
        self._name = name

        # lazy
        self._schema = None

    @classmethod
    def init_from_single_trace_kind(cls, single_trace_kind: SingleTraceKind):
        """
        Used when all members of the Finite are of the same trace kind
        Args:
            single_trace_kind:

        Returns:

        """
        obj = cls(single_trace_kind.get_name())
        obj._schema = single_trace_kind.get_schema()
        return obj

    def get_name(self)->str:
        return self._name

    def set_name(self, name:str)->None:
        """
        Can be used buy others to vote for their name or currently I am using it to name it according to trace kind plus slc
        Args:
            name:

        Returns:

        """
        self._name = name

    @abstractmethod
    def get_schema(self)->Dic:
        ...

    def extract_schema(self)->Dic:
        """
        To find schema based on the schema of the member traces
        Returns:

        """

