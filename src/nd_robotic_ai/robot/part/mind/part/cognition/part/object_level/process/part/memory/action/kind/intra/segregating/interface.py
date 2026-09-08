from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.component import \
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