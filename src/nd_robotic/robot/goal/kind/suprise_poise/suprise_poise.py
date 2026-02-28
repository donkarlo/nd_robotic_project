from nd_robotic.robot.goal.acceptance.kind.suprise.suprise import Suprise as SupriseAcceptance
from nd_robotic.robot.goal.goal import Goal
from nd_robotic.robot.state.kind.suprise import Suprise as SupriseState


class SurprisePoise(Goal):
    def __init__(self, desired_state: SupriseState, acceptance: SupriseAcceptance):
        """
        In this case desired is the same as tolerence value. it can be computed from the difference between prior and posterior
        Args:
            desired_state:
            acceptance:
        """
        Goal.__init__(self, desired_state, acceptance)
