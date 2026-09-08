from abc import ABC, abstractmethod

from nd_robotic_ai.robot.part.stimulus.observer.kind.mind_state_change.subscriber import \
    Subscriber as MindStateChangeSubscriber


class Publisher(ABC):
    @abstractmethod
    def publish_mind_state_change(self, mind_state_change:Minds) -> None:
        ...

    @abstractmethod
    def attach_mind_state_change_subcriber(self, subscriber: MindStateChangeSubscriber)->None:
        ...

    @abstractmethod
    def notify_mind_state_change_subscribers(self)->None:
        ...
