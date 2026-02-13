from nd_robotic.mind.cognition.process.kind.memory.composite.component import Component as MemoryComponent
from abc import ABC, abstractmethod

class Integrator(ABC):
    """
    In neuroscience at perceptual level which is a level higher than physiological layer integration is used to combine two components of memory (for example two trace groups )
    """
    def __init__(self, source_component:Component):
        self._source_component = source_component

        # cached
        self._integrated_components = None

    def get_integrated_components(self):
        if self._segregated_components is None:
            self._segregated_components()
        return self._segregated_components

    @abstractmethod
    def _set_integrated_components(self) -> List[MemoryComponent]:
        pass