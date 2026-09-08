from abc import ABC, abstractmethod
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.perception.trace.trace import Trace


class Subscriber(ABC):

    @abstractmethod
    def handle_trace_formation(self, trace:Trace) -> None:
        ...
