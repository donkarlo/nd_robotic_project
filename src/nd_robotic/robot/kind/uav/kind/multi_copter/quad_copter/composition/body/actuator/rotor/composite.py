from nd_robotic.robot.composition.component.kind.body.limb.kind.rotor.rotor import Rotor
from nd_robotic.robot.composition.composite import Composite as CompositeRobotUnit
from nd_robotic.robot.kind.uav.kind.multi_copter.quad_copter.composition.body.actuator.rotor.position import Position
from typing import List

class Composite(CompositeRobotUnit):
    def __init__(self):
        self._front_left_rotor = Rotor(Position.FRONT_LEFT)
        self._front_right_rotor = Rotor(Position.FRONT_RIGHT)
        self._rear_left_rotor = Rotor(Position.REAR_LEFT)
        self._rear_right_rotor = Rotor(Position.REAR_RIGHT)

        self.add_child(self._front_left_rotor)
        self.add_child(self._front_right_rotor)
        self.add_child(self._rear_left_rotor)
        self.add_child(self._rear_right_rotor)

    def get_rotors(self) -> List[Rotor]:
        return self.get_child_group_members()

    def get_front_left_rotor(self) -> Rotor:
        return self._front_left_rotor

    def get_front_right_rotor(self) -> Rotor:
        return self._front_right_rotor

    def get_rear_left_rotor(self) -> Rotor:
        return self._rear_left_rotor

    def get_rear_right_rotor(self) -> Rotor:
        return self._rear_right_rotor
