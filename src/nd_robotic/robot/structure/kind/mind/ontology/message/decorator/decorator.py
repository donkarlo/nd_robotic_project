from nd_robotic.robot.robot import Interface as MessageInterface
from nd_utility.oop.design_pattern.structural.decorator.decorator import Decorator as DesignPatternsDecorator


class Decorator(MessageInterface, DesignPatternsDecorator):
    def __init__(self, inner: StorageInterface):
        self._inner = inner