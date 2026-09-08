from abc import ABC, abstractmethod

from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.leaf.leaf import \
    Trace


class CreationSubscriber(ABC):
    @abstractmethod
    def handle_created_trace(self, trace: Trace) -> None: ...
