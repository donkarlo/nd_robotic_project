from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.leaf.leaf import \
    Interface as TraceInterface
from nd_utility.oop.design_pattern.structural.composition.decoration.decorator import Decorator as BaseDecorator


class Decorator(BaseDecorator, TraceInterface):
    """
    """

    def __init__(self, inner: TraceInterface):
        BaseDecorator.__init__(self, inner)
