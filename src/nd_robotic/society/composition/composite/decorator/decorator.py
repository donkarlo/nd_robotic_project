from nd_robotic_group_project.interface import Interface
from nd_utility.oop.design_pattern.structural.decorator.decorator import Decorator as BaseDecorator


class Decorator(BaseDecorator, Interface):
    def __init__(self, inner:Interface):
        super(BaseDecorator, self).__init__(inner)