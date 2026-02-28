from abc import ABC, abstractmethod

from nd_robotic.robot.action.composition.component import Component as ActionComponent
from nd_robotic.robot.action.feedback.feedback import Feedback
from nd_robotic.robot.goal.composite.component import Component as GoalComponent
from nd_utility.oop.design_pattern.structural.composition.leaf import Leaf as BaseLeaf


class Action(ActionComponent, BaseLeaf, ABC):
    """
    - Action is whatever consumes resorces such as energy or health(for example spare parts)
    This action can become so granular that to a action to change voltage in a rotor so in ROS we replaced Action for both Plan and COmmand and mission
    examples of actions the subclasses should support:
    - body
        - Goto

    - Mind
        - memory segregating
        - Memory
            - memorize
            - remember
    """

    def __init__(self, goal: GoalComponent):
        ActionComponent.__init__(self)
        BaseLeaf.__init__(self)
        self._goal = goal
        self._feedback = None

    @abstractmethod
    def run(self) -> Feedback:
        """
        This run will be propegated to top or mabe bottom actions
        Returns:

        """
        pass

    def get_feedback(self) -> Feedback:
        return self._feedback

    def get_goal(self) -> GoalComponent:
        return self._goal
