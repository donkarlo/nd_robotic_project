from nd_robotic.robot.robot import Collection
from nd_robotic.robot.robot import Rotor
from nd_robotic.robot.robot import RotorPosition


class RotorSet(Collection):
    def __init__(self, rotor:Rotor):
        rotor_class = rotor.__class__
        self._front_left_rotor = rotor_class(RotorPosition.FRONT_LEFT)
        self._front_right_rotor = rotor_class(RotorPosition.FRONT_RIGHT)
        self._rear_left_rotor = rotor_class(RotorPosition.REAR_LEFT)
        self._rear_right_rotor = rotor_class(RotorPosition.REAR_RIGHT)
        super().__init__([self._front_left_rotor, self._front_right_rotor, self._rear_left_rotor, self._rear_right_rotor])

    def get_actuator_set(self) -> Collection:
        return self._actuator_set
    def get_front_left_rotor(self) -> Rotor:
        return self._front_left_rotor
    def get_front_right_rotor(self) -> Rotor:
        return self._front_right_rotor
    def get_rear_left_rotor(self) -> Rotor:
        return self._rear_left_rotor
    def get_rear_right_rotor(self) -> Rotor:
        return self._rear_right_rotor