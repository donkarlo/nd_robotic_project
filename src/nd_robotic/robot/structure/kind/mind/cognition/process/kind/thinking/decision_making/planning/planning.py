from nd_robotic.robot.action.action import Action
from nd_robotic.robot.action.composite.composite import Composite as CompositeAction
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.kind.explicit.kind.long_term.episodic.autobigraphical.kind.event_specific_knowledge.kind.multi_model.building_single_modality_forcasting_models import \
    BuildingSingleModalityForcastingModels as BuildingSingleForcastingModelFromEpisodeAction
from nd_robotic.robot.goal.composite.composite import Composite as CompositeGoal
from nd_robotic.robot.goal.kind.suprise_poise.suprise_poise import SuprisePoise


class Planning:
    """
    tex:
        cite:
            - "Automated planning and scheduling":
                url: "https://en.wikipedia.org/wiki/Automated_planning_and_scheduling"
    """
    def __init__(self, composite_goal: CompositeGoal):
        self._composite_goal = composite_goal

        # adding suprise poise goal_gain as the goal_gain for the root action
        self._composite_action = CompositeAction(Action(self._composite_goal))

    def get_composite_action(self) -> CompositeAction:
        root_action_goal = self._composite_action.get_leaf().get_goal()
        if isinstance(root_action_goal, SuprisePoise):
            # if the system has no human goal or it is not in human controled teleportation sensory-motor recording, then it is in idle mode and it can build forcating models for each moodalirty such as GPS and LIDAR
            if len(root_action_goal.get_children()) == 1:
                self._composite_action.add_child(BuildingSingleForcastingModelFromEpisodeAction())
        return self._composite_action

    def get_predicted_success_rate(self) -> float:
        pass
