from tensorflow.python.ops.gen_array_ops import deep_copy

from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.composite import \
    Composite as MemoryComposite
from nd_robotic_ai.robot.part.action.composition.composite import \
    Composite as ActionComposite
from nd_robotic_ai.robot.part.goal.composition.component import \
    Component as GoalComponent
from nd_robotic_ai.robot.part.goal.composition.composite import \
    Composite as GoalComposite
from nd_robotic_ai.robot.part.goal.plan.plan import \
    Plan as SemanticPlan
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.thinking.part.planning.planning import \
    Planning


class Plan(MemoryComposite):
    """
    Maybe plan must be changed according to action feedback
    """

    def __init__(self):
        MemoryComposite.__init__(self)

        self._semantic_plan = deep_copy(SemanticPlan())

        self._working_goal_composite = self._semantic_plan.get_goal_composite()
        self._working_action_composite = self._semantic_plan.get_action_composite()

        MemoryComposite.add_child(self._working_goal_composite)
        MemoryComposite.add_child(self._working_action_composite)

        self._planning = Planning()
        self.attach_subscriber(self._planning)

    def get_working_action_composite(self) -> ActionComposite:
        return self._working_action_composite

    def get_working_goal_composite(self) -> GoalComposite:
        return self._working_goal_composite

    def attach_goal(self, parent_goal: GoalComposite, child_goal: GoalComponent) -> None:
        """
        We can just attach goals and not actions. Planning in mind>process>thinking>decision making  makes a classification action
        Args:
            parent_goal:
            child_goal:

        Returns:

        """
        self._working_goal_composite.get_child(parent_goal).add_child(child_goal)
        self.notify_subscribers(self)
