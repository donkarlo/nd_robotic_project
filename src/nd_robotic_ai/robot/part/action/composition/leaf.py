from abc import ABC

from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.leaf.leaf import \
    Trace
from nd_robotic_ai.robot.part.action.feedback.feedback import Feedback
from nd_robotic_ai.robot.part.goal.composition.component import Component as GoalComponent


class Leaf(Trace, ABC):
    def __init__(self, goal: GoalComponent):
        self._goal = goal
        self._feedback = None

    def get_feedback(self) -> Feedback:
        return self._feedback

    def get_goal(self) -> GoalComponent:
        return self._goal
