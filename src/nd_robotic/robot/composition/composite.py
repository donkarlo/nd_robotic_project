from nd_robotic.robot.composition.component.component import Component as RobotComponent
from nd_utility.oop.design_pattern.structural.composition.composite import Composite as BaseComposite

class Composite(RobotComponent, BaseComposite):
    """
    RotorComposite unit shows the flow of information or messages or signals, it is usually
    """

    def __init__(self):
        BaseComposite.__init__(self)
        RobotComponent.__init__(self)