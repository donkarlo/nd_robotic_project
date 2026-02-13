
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.component import \
    Component as MemoryComponent
from typing import List

from abc import ABC, abstractmethod

class Interface(ABC):

    @abstractmethod
    def __init__(self, source_memory_component: MemoryComponent):
        ...

    @abstractmethod
    def segregate(self)->None:
        ...

    @abstractmethod
    def get_segregated_components(self)->List[MemoryComponent]:
        ...