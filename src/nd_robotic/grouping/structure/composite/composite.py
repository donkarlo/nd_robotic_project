from nd_robotic.grouping.structure.composite.component import Component
from nd_robotic.grouping.structure.group import Group
from nd_utility.oop.design_pattern.structural.composite.composite import Composite as BaseComposite


class Composiet(Component, BaseComposite):
    def __init__(self, group:Group):
        BaseComposite.__init__(self, group)