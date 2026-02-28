from nd_robotic.robot.goal.composite.component import Component as GoalComponent
from nd_robotic.robot.goal.goal import Goal
from nd_utility.oop.design_pattern.structural.composition.composite import Composite as BaseComposite



class Composite(GoalComponent, BaseComposite):
    def __init__(self, goal:Goal, name: str):
        """

        Args:
            internal_trace_group: can be None to only host the link (child) to the next inner_experiment (trace action_potential_group here) or composition (only link/child or a trace action_potential_group)
            name:
        """
        self._goal = goal
        GoalComponent.__init__(self, name)
        BaseComposite.__init__(self, goal, name)