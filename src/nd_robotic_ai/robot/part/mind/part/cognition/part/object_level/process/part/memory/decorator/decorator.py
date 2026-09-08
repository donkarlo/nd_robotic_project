
from nd_utility.oop.design_pattern.structural.decoration.decorator import Decorator as BaseDecorator

from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.component import Component as MemoryComponent


class Decorator(MemoryComponent, BaseDecorator):
    def __init__(self, inner: MemoryComponent):
        MemoryComponent.__init__(self)
        BaseDecorator.__init__(self, inner)
