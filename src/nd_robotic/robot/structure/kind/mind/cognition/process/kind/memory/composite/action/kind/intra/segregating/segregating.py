from typing import List, Optional
from abc import ABC, abstractmethod
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.action.kind.intra.segregating.interface import Interface as SegregationInterface
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.component import Component as MemoryComponent


class Segregating(SegregationInterface, ABC):
    """
    Neurological term for seprating different senses that we use here for a trace action_potential_group to seprate it should cover
    - Segregating is an effort to reduce suprise
    - separating modalities
    - clustering

    """
    def __init__(self, source_memory_component: MemoryComponent):
        self._source_memory_component = source_memory_component

        # cached
        self._segregated_components:Optional[List[MemoryComponent]] = None

    def get_segregated_components(self)->List[MemoryComponent]:
        if self._segregated_components is None:
            self._segregated_components = []
            self._build_segregated_components()
        return self._segregated_components

    @abstractmethod
    def _build_segregated_components(self)->None: ...

