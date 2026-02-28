from nd_robotic.robot.composition.component.kind.body.limb.kind.rotor.rotor import Rotor
from nd_robotic.robot.kind.uav.kind.multi_copter.quad_copter.composition.body.actuator.rotor.composite import Group as RotorGroup
from nd_robotic.robot.kind.uav.uav import Uav


class QuadCopter(Uav):
    def __init__(self):
        Uav.__init__(self)
        rotor = [Rotor(Positions.)]
        rotor_group = RotorGroup()

        self.add_child()