from nd_robotic_ai.robot.part.action.action import Action
from nd_robotic_ai.robot.composition.kind.body.limb.kind.rotor.action.change_direction.mode import Mode


class ChangeDirection(Action):
    def __init__(self):
        Action.__init__(self)

    def set_mode(self, mode: Mode) -> None:
        self._mode = mode