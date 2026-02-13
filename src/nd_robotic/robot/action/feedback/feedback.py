from abc import ABC, abstractmethod

from nd_robotic.robot.action.feedback.resource_gain.resource_gain import ResourceGain as ResourceGain
from nd_robotic.robot.action.feedback.goal_gain.goal_gain import GoalGain as GoalGain


class Feedback(ABC):
    def __init__(self, goal_gain: GoalGain, resource_gain: ResourceGain):
        self._goal_gain = goal_gain
        self._resource_gain = resource_gain

    @abstractmethod
    def get_value(self) -> float:
        """
        This method should provide a soltion to convert the discrepence between goal_gain gain and resource_gain gain
        """
        ...
