from abc import ABC, abstractmethod

from nd_utility.data.kind.dic.dic import Dic
from nd_robotic_ai.robot.composition.kind.mind.meta_cognition.cognition.process.composition.child.memory.composition.trace.kind.core.kind import Kind as  SingleTraceKind


class Kind(ABC):
    """
    Should represent a relationship that relates a society of traces together. Such as Iranian in Human being
    """
    def __init__(self, name: str):
        self._name = name

        # lazy
        self._schema = None

    @classmethod
    def init_from_single_trace_kind(cls, single_trace_kind: SingleTraceKind):
        """
        Used when all members of the Finite are of the same trace_formation classification
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
        Can be used buy others to vote for their title or currently I am using it to title it according to trace_formation classification plus slc
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

