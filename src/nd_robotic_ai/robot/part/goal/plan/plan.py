from nd_robotic_ai.robot.part.action.composition.composite import \
    Composite as ActionComposite
from nd_robotic_ai.robot.part.goal.composition.composite import \
    Composite as GoalComposite
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.long_term.part.semantic.sematic import \
    Semantic


class Plan(Semantic):
    """
    Maybe plan must be changed according to action feedback
    """

    def __init__(self):
        Semantic.__init__(self)

        self._goal_composite.add_child(GoalComposite())
        self._action_composite.add_child(ActionComposite())
        self.add_child(self._goal_composite)
        self.add_child(self._action_composite)

    def get_goal_composite(self) -> GoalComposite:
        return self._goal_composite

    def get_action_composite(self) -> ActionComposite:
        return self._goal_composite
