from nd_robotic.robot.structure.kind.mind.action.action import Action as MindAction
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.component import \
    Component as MemoryComponent


class Action(MindAction):
    def __init__(self, memory_component: MemoryComponent):
        self._memory_component = memory_component

    def get_memory_component(self) -> MemoryComponent:
        return self._memory_component
