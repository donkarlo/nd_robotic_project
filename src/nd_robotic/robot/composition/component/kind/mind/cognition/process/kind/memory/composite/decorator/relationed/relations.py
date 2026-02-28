from nd_robotic.mind.cognition.process.kind.memory.composite.component import Component as MemoryComponent


class Relations:
    def __init__(self, related_component: List[MemoryComponent]):
        """
        The idea was to define the relation between child and parent for example it is segregated for different sensor modalities but it can be used to define as any relation between this component and others
        Args:
            related_component:
        """
        self._related_components = related_components

    def get_related_components(self)->List[MemoryComponent]:
        return self._related_components