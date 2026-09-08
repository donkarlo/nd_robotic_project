from abc import ABC, abstractmethod

from nd_robotic_ai.robot.part.stimulus.observer.kind.mind_state_change.mind_state_change import MindStateChange


class Subscriber(ABC):

    @abstractmethod
    def handle_mind_state_change(self, mind_state_change: MindStateChange) -> None:
        ...
