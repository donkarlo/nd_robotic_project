from nd_robotic.robot.composition.component.kind.body.nervous_system.composition.central.composition.brain.brain import Brain
from nd_robotic.robot.composition.component.kind.body.nervous_system.composition.central.composition.retina.retina import Retina
from nd_robotic.robot.composition.component.kind.body.nervous_system.composition.central.composition.spinal_cord.spinal_cord import SpinalCord
from nd_robotic.robot.composition.composite import Composite as RobioticCompositeUnit


class Central(RobioticCompositeUnit):
    def __init__(self):
        self.add_child(Brain())
        self.add_child(SpinalCord())
        self.add_child(Retina())