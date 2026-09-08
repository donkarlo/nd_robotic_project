from abc import ABC, abstractmethod

from nd_math.probability.bayesian.observation import Observation
from nd_robotic_ai.robot.part.stimulus.observer.kind.trace_formation.subscriber import \
    Subscriber as PerceptionSubscriber


class Publisher(ABC):
    @abstractmethod
    def publish_trace_formation(self, observation: Observation) -> None:
        ...

    @abstractmethod
    def attach_trace_formation_subcriber(self, trace_formation_subscriber: PerceptionSubscriber) -> None:
        ...

    @abstractmethod
    def notify_trace_formation_subscribers(self) -> None:
        ...
