from nd_robotic.robot.state.interface import Interface as StateInterface
from nd_utility.oop.design_pattern.structural.decorator.decorator import Decorator as BaseDecorator


class Decorator(BaseDecorator, StateInterface):
    def __init__(self, inner: StateInterface):
        BaseDecorator.__init__(self, inner)