from nd_robotic_ai.robot.composition.kind.mind.meta_cognition.cognition.process.composition.child.memory.composition.action.action import Action
from nd_robotic_ai.robot.composition.kind.mind.meta_cognition.cognition.process.composition.child.memory.composition.component import Component as MemoryComponent


class Memorize(Action):
    def __init__(self, component_to_memorize: MemoryComponent):
        self._component_to_memorize = component_to_memorize

    def get_component_to_memorize(self)->MemoryComponent:
        return self._component_to_memorize