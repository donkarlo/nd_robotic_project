
from nd_robotic.robot.robot import Goal
from nd_robotic.robot.robot import Composite
from typing import Optional


class Experience:
    def __init__(self, mission: Goal, executed_plan: Composite, shared_stack:Stack, modality_group: ModalityGroup, name:Optional[str]=None):
        """
        https://en.wikipedia.org/wiki/Experience
        Unlike scenario, you dont need world here, all is in event_specific_knowledge current_level 0 about world understanding of the robot. Scenario is human view for testing
        Args:
            mission:
            executed_plan:
            shared_stack: all modalities are in a trace_storage file
            modality_group: for example current_level 0 is sensory action_potential_group, current_level 1 is clusters
        """
        # initial pre_plan
        self._shared_stack = shared_stack
        self._modality_collection = modality_group
        self._mission = mission
        self._executed_plan = executed_plan
        self.__name = name

    def get_modality_collection(self) -> ModalityGroup:
        return self._modality_collection

    def get_name(self) -> Optional[str]:
        return self.__name

    def find_cycles(self):
        pass
