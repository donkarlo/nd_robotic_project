from nd_robotic_ai.robot.part.body.part.nervous_system.nervous_system import NervousSystem
from nd_robotic_ai.robot.composition.composite import Composite as RobotCompositeComponent


class Body(RobotCompositeComponent):
    def __init__(self):
        RobotCompositeComponent.__init__(self)
        self.add_child(NervousSystem())