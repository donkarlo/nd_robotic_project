# from nd_robotic_ai.robot.classification.uav.classification.multi_copter.quad_copter.classification.body.actuator.rotor.composition import Train as RotorGroup
from nd_robotic_ai.robot.kind.uav.uav import Uav


class QuadCopter(Uav):
    def __init__(self):
        Uav.__init__(self)
        # rotor = [Rotor(Positions.)]
        # rotor_group = RotorGroup()
        #
        # self.add_child()