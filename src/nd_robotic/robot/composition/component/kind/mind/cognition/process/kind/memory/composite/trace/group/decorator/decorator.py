from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.trace.group.interface import Interface as TraceGroupInterface
from nd_utility.oop.design_pattern.structural.decorator.decorator import Decorator as BaseDecorator


class Decorator(BaseDecorator, TraceGroupInterface):
    """
    """

    def __init__(self, inner: TraceGroupInterface):
        BaseDecorator.__init__(self, inner)
