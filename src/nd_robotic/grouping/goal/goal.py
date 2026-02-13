from nd_math.linear_algebra.tensor.vector.vector_representable import VectorRepresentable
from nd_robotic.robot.robot import AcceptanceCriterion
from nd_utility.oop.design_pattern.structural.composite.example import Leaf as BaseLeaf


class Goal(BaseLeaf, VectorRepresentable):
    """
    Represents a bottom state and its acceptance criterion.
    """

    def __init__(self, desired_state: VectorRepresentable, acceptance: AcceptanceCriterion):
        self._desired_state = desired_state
        self._acceptance = acceptance

    def is_achieved(self, current_state: VectorRepresentable) -> bool:
        return self._acceptance.is_satisfied(current_state, self._desired_state)

    def get_desired_state(self) -> VectorRepresentable:
        return self._desired_state

    def get_acceptance(self) -> AcceptanceCriterion:
        return self._acceptance