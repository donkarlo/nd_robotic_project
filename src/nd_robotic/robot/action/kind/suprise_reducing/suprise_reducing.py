from nd_math.probability.distribution.discrepancy.kind.divergence.kind.kullback_leibler.kullback_leibler import \
    KullbackLeiblerDivergence
from nd_robotic.robot.action.action import Action
from nd_robotic.robot.action.feedback.feedback import Feedback
from nd_robotic.robot.goal.acceptance.kind.suprise.suprise import Suprise as SupriseAcceptance
from nd_utility.oop.inheritance.overriding.override_from import override_from


class SupriseReducing(Action):
    """
    Mental action:
        Reduce suprise either by
            - improving the forcasting models
    Physical:
        changing the world with actuators
    """

    def __init__(self):
        acceptance_threshold = 0.5
        discrepancy_method = KullbackLeiblerDivergence()
        acceptance = SupriseAcceptance(discrepancy_method)
        goal = SupriseReducing(acceptance)
        Action.__init__(self, goal)

    @override_from(Action)
    def run(self)->Feedback:
        pass