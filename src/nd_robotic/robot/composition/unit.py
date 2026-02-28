from nd_robotic.robot.composition.component.component import Component as RobotComponent
from nd_utility.oop.design_pattern.structural.composition.leaf import Leaf as BaseLeaf

class Unit(RobotComponent, BaseLeaf):
    def __init__(self):
        """
        This must paly the role of the link in URDF
        """
        RobotComponent.__init__(self)
        BaseLeaf.__init__(self)