from nd_robotic.robot.robot import Interface
from nd_utility.oop.design_pattern.structural.decorator.decorator import Decorator


class Decorator(Decorator, Interface):
    def __init__(self, sensor):
        super(Decorator, self).__init__(sensor)