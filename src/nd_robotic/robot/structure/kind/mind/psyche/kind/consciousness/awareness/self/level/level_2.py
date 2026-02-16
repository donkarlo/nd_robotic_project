from nd_robotic.robot.robot import Level
from typing import Annotated, List, override

UnitInterval = Annotated[float, "0.0 ≤ x ≤ 1.0"]


# -------------------------
# LowerAndHigherAwareLayer 2 – Mirror/representation-based self-identification
# -------------------------
class Level2(Level):
    """
    Understands that a representation (mirror, video, avatar, sound, odor) refers to self.
    """

    def test_mirror_mark(self) -> UnitInterval:
        """
        Classic mark test with reflection/pose alignment (or simulated equivalent).
        """
        return 0.0

    def test_video_temporal_contingency(self) -> UnitInterval:
        """
        Self-recognition under temporal offsets (live vs. delayed feed), testing whether
        the agent still maps the representation to self across small delays.
        """
        return 0.0

    def test_crossmodal_self_mapping(self) -> UnitInterval:
        """
        Associates self-unique signatures across modality_group (voice/propeller-harmonics,
        RF/odometry trace, odor tag), discriminating own signals from conspecifics.
        """
        return 0.0

    @override
    def run_tests(self) -> List[float]:
        v1 = self.test_mirror_mark()
        v2 = self.test_video_temporal_contingency()
        v3 = self.test_crossmodal_self_mapping()
        return [v1, v2, v3]