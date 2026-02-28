from nd_robotic.robot.composition.component.kind.body.nervous_system.composition.central.central import Central
from nd_robotic.robot.composition.component.kind.body.nervous_system.composition.peripheral.peripheral import Peripheral
from nd_robotic.robot.composition.composite import Composite as RobotCompositeUnit


class NervousSystem(RobotCompositeUnit):
    def __init__(self):
        self.add_child(Central())
        self.add_child(Peripheral())