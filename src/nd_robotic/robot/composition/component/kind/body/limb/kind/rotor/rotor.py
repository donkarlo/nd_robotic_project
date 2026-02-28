from nd_robotic.robot.action.action import Action
from nd_robotic.robot.composition.component.kind.body.limb.limb import Limb
from typing import Optional

from nd_robotic.robot.composition.component.kind.body.limb.kind.rotor.action.change_arming_mode.change_arming_mode import ChangeArmingMode
from nd_robotic.robot.composition.component.kind.body.limb.kind.rotor.action.change_arming_mode.mode import Mode as ArmMode
from nd_robotic.robot.composition.component.kind.body.limb.kind.rotor.action.change_direction.mode import Mode as DirectionMode
from nd_robotic.robot.composition.component.kind.body.limb.kind.rotor.action.change_direction.change_direction import ChangeDirection


class Rotor(Limb):
    def __init__(self, direction_mode:DirectionMode):
        ChangeArmingMode().set_mode(ArmMode.DISARMED)
        self._direction_mode = ChangeDirection(DirectionMode.COLOCK_WISE)
        self._valid_actions = [ChangeArmingMode, default_direction_mode]
        Limb.__init__(valid_actions)


