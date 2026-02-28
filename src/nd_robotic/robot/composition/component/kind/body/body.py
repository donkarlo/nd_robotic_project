from nd_robotic.robot.composition.composite import Composite as RobotUnitComposite
from nd_robotic.robot.composition.component.kind.body.nervous_system.nervous_system import NervousSystem


class Body(RobotUnitComposite):
    def __init__(self):
        self.add_child(NervousSystem())