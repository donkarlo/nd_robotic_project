from abc import abstractmethod

from nd_robotic_ai.robot.part.action.feedback.composition.composite import \
    Composite as FeedbackComposite
from nd_robotic_ai.robot.part.action.feedback.part.goal_gain.goal_gain import \
    GoalGain as GoalGain
from nd_robotic_ai.robot.part.action.feedback.part.resource_gain.resource_gain import \
    ResourceGain as ResourceGain


class Feedback(FeedbackComposite):
    def __init__(self):
        FeedbackComposite.__init__(self)
        self._goal_gain = GoalGain()
        self._resource_gain = ResourceGain()

        self.add_child(self._goal_gain)
        self.add_child(self._resource_gain)

    @abstractmethod
    def get_value(self) -> float:
        """
        This method should provide a soltion to convert the discrepence between goal_gain gain and resource_gain gain
        """
        ...
