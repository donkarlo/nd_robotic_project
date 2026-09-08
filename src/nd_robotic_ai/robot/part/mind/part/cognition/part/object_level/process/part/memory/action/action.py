from nd_robotic_ai.robot.composition.kind.mind.action.action import Action as MindAction
from nd_robotic_ai.robot.composition.kind.mind.meta_cognition.cognition.process.composition.child.memory.composition.component import \
    Component as MemoryComponent


class Action(MindAction):
    def __init__(self, memory_component: MemoryComponent):
        self._memory_component = memory_component

    def get_memory_component(self) -> MemoryComponent:
        return self._memory_component
