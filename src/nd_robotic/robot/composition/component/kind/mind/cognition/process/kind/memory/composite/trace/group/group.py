from typing import List, Optional, Any
from functools import cache

from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.component import Component as MemoryComponent
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.trace.group.kind.core.kind import Kind  as TraceGoupKind
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.trace.trace import Trace
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.trace.group.interface import Interface as GroupInterface
from nd_utility.data.kind.group.group import Group as BaseGroup
from nd_utility.oop.design_pattern.structural.composition.example import Leaf as BaseLeaf


class Group(MemoryComponent, BaseGroup, BaseLeaf, GroupInterface):
    def __init__(self, traces:Optional[List[Trace]], name:Optional[str]):
        #just to comply with interface
        BaseGroup.__init__(self, traces)
        MemoryComponent.__init__(self, name)
        BaseLeaf.__init__(self)

        self._kind: Optional[TraceGoupKind] = None

        # lazy loading
        self._formatted_data_list = None

    @classmethod
    def init_by_traces_and_kind_and_name(cls, traces: Optional[List[Trace]], kind:Optional[TraceGoupKind], name: Optional[str])-> "Finite":
        obj = cls(traces, name)
        obj._kind = kind
        return obj

    def get_traces(self) -> Optional[List[Trace]]:
        return self.get_members()

    def get_kind(self)-> TraceGoupKind:
        if self._kind is None:
            self._kind = self.extract_dominant_kind_from_member_trace_kind()
        return self._kind

    def set_name(self, name:str)->None:
        """
        Maybe the title is voted among the mebers of the action_potential_group
        Args:
            name:

        Returns:

        """
        self._name = name

    def extract_dominant_kind_from_member_trace_kind(self)-> TraceGoupKind:
        ...

    @cache
    def get_formatted_data_list(self)->List[Any]:
        if self._formatted_data_list is None:
            self._formatted_data_list = []
            for trace in self.get_traces():
                self._formatted_data_list.append(trace.get_formatted_data())
            return self._formatted_data_list

    def stringify(self) -> str:
        return ""

    def get_traces(self)->List[Trace]:
        """
        Just a nick title
        Returns:

        """
        return self.get_members()





