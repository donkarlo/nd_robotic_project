from nd_robotic.grouping.structure.composite.component import Component
from nd_utility.data.kind.group.group import Group as UtilityGroup
from nd_utility.oop.design_pattern.structural.composite.leaf import Leaf


class Group(Component, UtilityGroup ,  Leaf):
    """
    A set of robots whose states are intra related through commands
    """
    def __init__(self, members, name:str):
        UtilityGroup.__init__(self, members)
        Leaf.__init__(self, name)