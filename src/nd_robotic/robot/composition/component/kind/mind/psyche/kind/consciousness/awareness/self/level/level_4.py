from nd_robotic.robot.robot import Level
from typing import Annotated, List, override

UnitInterval = Annotated[float, "0.0 ≤ x ≤ 1.0"]


# -------------------------
# LowerAndHigherAwareLayer 4 – Meta-self (metacognition, self-concept)
# -------------------------
class Level4(Level):
    """
    Represents self as an enduring entity with traits, knowledge states, and limits.
    """

    def test_metacognitive_uncertainty(self) -> UnitInterval:
        """
        Opts to 'decline' or seek information when confidence is low; calibrated confidence
        correlates with actual accuracy across tasks (proper scoring).
        """
        return 0.0

    def test_self_concept_reporting(self) -> UnitInterval:
        """
        Reports stable internal properties (capabilities, roles, resource_gain budgets)
        and updates them coherently after evidence (self-transformer_model revision).
        """
        return 0.0

    def test_recursive_toM(self) -> UnitInterval:
        """
        Second-order belief reasoning (I think that you think ...), demonstrated by
        strategic behavior in signaling/hiding resources in competitive/cooperative tasks.
        """
        return 0.0

    @override
    def run_tests(self) -> List[float]:
        v1 = self.test_metacognitive_uncertainty()
        v2 = self.test_self_concept_reporting()
        v3 = self.test_recursive_toM()
        return [v1, v2, v3]