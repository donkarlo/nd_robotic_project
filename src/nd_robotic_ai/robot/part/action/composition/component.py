from abc import ABC, abstractmethod

from nd_robotic_ai.robot.part.action.feedback.feedback import Feedback
from nd_utility.oop.design_pattern.structural.composition.component import Component as BaseComponent


class Component(BaseComponent, ABC):
    """
    """

    def __init__(self):
        BaseComponent.__init__(self)

    @abstractmethod
    def run(self):
        ...

    @abstractmethod
    def get_feedback(self) -> Feedback:
        ...
