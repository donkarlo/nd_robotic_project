from nd_robotic.mind.cognition.process.kind.memory.composite.component import Component as MemoryComponent
from nd_robotic.mind.cognition.process.kind.memory.composite.decorator.decorator import Decorator
from nd_robotic.mind.cognition.process.kind.memory.composite.decorator.relationed.relations import Relations


class Relationed(Decorator):
    def __init__(self, inner: MemoryComponent, relationes:Relations):
        self._relations = relationes

    def get_relations(self)->Relations:
        return self._relations