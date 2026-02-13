from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.action.action import Action
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.component import Component as MemoryComponent


class Memorize(Action):
    def __init__(self, component_to_memorize: MemoryComponent):
        self._component_to_memorize = component_to_memorize

    def get_component_to_memorize(self)->MemoryComponent:
        return self._component_to_memorize