from nd_robotic.robot.action.composite.component import Component as ActionComponent
from nd_robotic.robot.action.feedback.feedback import Feedback
from nd_robotic.grouping.action.action import Action
from nd_utility.oop.design_pattern.structural.composite.composite import Composite as BaseComposite


class Composite(ActionComponent, BaseComposite):
    """
    - is a flat set of actions in composite tree
    Composite is a set of actions to be taken to achieve a initial_mission
    - This class is created beacause in a inner_experiment we might have two different plans that can acomplish the same initial_mission
    - https://en.wikipedia.org/wiki/Goal_setting
        - GoalGain setting involves the development of an action initial_plan designed in order to motivate and guide a person or action_potential_group toward a composite_goal
    """

    def __init__(self, action: Action):
        BaseComposite.__init__(self, action, None)
        ActionComponent.__init__(self, action.get_goal(), None)
        # this and aliaz for BaseComposite(self)._leaf
        self._action = action

    def run(self) -> Feedback:
        self._feedback = self._action.run()

        for child in BaseComposite.get_children(self):
            child.run()

        return self._feedback
