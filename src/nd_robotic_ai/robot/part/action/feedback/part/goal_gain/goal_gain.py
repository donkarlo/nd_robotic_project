from nd_robotic_ai.robot.part.action.feedback.composition.leaf import Leaf

class GoalGain(Leaf):
    def __init__(self, value: float):
        Leaf.__init__(self)
        self._value = value

    def get_value(self) -> float:
        return self._value