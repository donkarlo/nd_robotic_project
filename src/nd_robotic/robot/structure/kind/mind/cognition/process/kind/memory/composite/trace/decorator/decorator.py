from nd_robotic.robot.robot import Interface as TraceInterface
from nd_utility.oop.design_pattern.structural.decorator.decorator import Decorator as BaseDecorator


class Decorator(BaseDecorator, TraceInterface):
    """
    """

    def __init__(self, inner:TraceInterface):
        BaseDecorator.__init__(self, inner)


