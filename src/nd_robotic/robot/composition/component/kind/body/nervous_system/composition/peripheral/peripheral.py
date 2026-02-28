from nd_robotic.robot.composition.component.kind.body.nervous_system.composition.peripheral.kind.autonomic.autonomic import \
    Autonomic
from nd_robotic.robot.composition.component.kind.body.nervous_system.composition.peripheral.kind.somatic.somatic import Somatic
from nd_robotic.robot.composition.component.kind.body.nervous_system.composition.peripheral.kind.enteric.enteric import \
    Enteric
from nd_robotic.robot.composition.composite import Composite as RobotCompositeUnit


class Peripheral(RobotCompositeUnit):
    def __init__(self):
        self.add_child(Somatic())
        self.add_child(Enteric())
        self.add_child(Autonomic())