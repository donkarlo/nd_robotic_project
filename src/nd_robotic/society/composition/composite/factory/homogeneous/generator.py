from nd_robotic_group_project.group import Group
from nd_robotic.mind.cognition.process.kind.memory.composite.component import Component as MemoryComponent
from nd_robotic.robot.robot import Robot
from typing import List, Optional
import copy

class Generator:
    def __init__(self, prototype:Robot, memory_roots:List[MemoryComponent], names:Optional[List])->None:
        self._prototype = prototype
        self._memory_component_roots = memory_roots
        self._names = names
        if self._names is None:
            self.__assign_names()

    def __assign_names(self)->None:
        self._names = []
        for counter in range (1, len(self._memory_component_roots)):
            self._names.append(counter)

    def build_memory(self):
        pass

    def get_robots_by_prototype_with_given_name_and_memory(self, sample_robot: Robot, names:Optional[List[str]]=None)->Group:
        """

        Args:
            names:

        Returns:

        """
        robots = []
        self._names = names
        for counter, name in enumerate(self._names):
            # TODO: check uniqness of the __name
            copied_robot = copy.deepcopy(sample_robot)
            copied_robot.set_name(name)
            robots.append(copied_robot)
        return Group(robots)

