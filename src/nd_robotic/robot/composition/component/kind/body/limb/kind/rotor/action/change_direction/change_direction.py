from nd_robotic.robot.action.action import Action
from nd_robotic.robot.composition.component.kind.body.limb.kind.rotor.action.change_direction.mode import Mode


class ChangeDirection(Action):
    def __init__(self):
        Action.__init__(self)

    def set_mode(self, mode: Mode) -> None:
        self._mode = mode