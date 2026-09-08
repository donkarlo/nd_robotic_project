from nd_robotic_ai.robot.kind.uav.uav import Uav


class MultiCopter(Uav):
    def __init__(self, rotors_number:int):
        Uav.__init__(self)
        