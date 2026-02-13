from nd_robotic.robot.robot import Level
from typing import Annotated, List, override

UnitInterval = Annotated[float, "0.0 ≤ x ≤ 1.0"]


# -------------------------
# LowerAndHigherAwareLayer 3 – Perspective-taking and episodic awareness
# -------------------------
class Level3(Level):
    """
    Treats 'self' as a subject situated in time and relative to others' viewpoints.
    """

    def test_perspective_taking(self) -> UnitInterval:
        """
        Distinguishes what another agent can/cannot perception (line-of-sight, occlusion),
        adapting str_path/communicating accordingly.
        """
        return 0.0

    def test_episodic_memory_www(self) -> UnitInterval:
        """
        'What-Where-When' recall: retrieves episodic content + location + temporal index,
        verified by counter-queries and consistency checks.
        """
        return 0.0

    def test_future_need_planning(self) -> UnitInterval:
        """
        Plans for a future state in which resources/tools are required later but not now
        (deferred goal_gain/tool caching without immediate payoff).
        """
        return 0.0

    @override
    def run_tests(self) -> List[float]:
        v1 = self.test_perspective_taking()
        v2 = self.test_episodic_memory_www()
        v3 = self.test_future_need_planning()
        return [v1, v2, v3]