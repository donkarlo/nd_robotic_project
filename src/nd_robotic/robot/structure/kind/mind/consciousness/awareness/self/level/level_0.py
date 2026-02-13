from nd_robotic.robot.robot import Level
from typing import Annotated, List, override

UnitInterval = Annotated[float, "0.0 ≤ x ≤ 1.0"]

class Level0(Level):
    """
    The organism distinguishes between itself and the world.
    """
    def test_immunoligibgical_self(self)->float:
        """
        distinction (immune system rejects foreign tissue).
        Returns:

        """
        return 0.0

    def test_tactile_reafference_suppression(self)->float:
        """
        animals ignore sensations from self-generated actions (e.g., fish Predicting their own electrosensory discharges).
        Returns:

        """
        return 0.0

    def test_proprioceptive_consistency(self)->float:
        """
        ability to correct body posture or maintain equilibrium.
        Returns:

        """
        return 0.0

    @override
    def run_tests(self)->List[float]:
        val1 = self.test_immunoligibgical_self()
        val2 = self.test_tactile_reafference_suppression()
        val3 = self.test_proprioceptive_consistency()
        return [val1, val2, val3]