from nd_robotic_ai.mind.cognition.process.kind.memory.composite.component import Component as MemoryComponent


class Relations:
    def __init__(self, related_component: List[MemoryComponent]):
        """
        The idea was to define the relationship between classification and parent for example it is segregated for different sensory modalities but it can be used to define as any relationship between this component and others
        Args:
            related_component:
        """
        self._related_components = related_components

    def get_related_components(self)->List[MemoryComponent]:
        return self._related_components