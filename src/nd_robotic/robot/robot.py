from abc import ABC
from typing import Optional

from nd_robotic.robot.goal.composite.component import Component as ComponentGoal
from nd_robotic.robot.goal.composite.composite import Composite as CompositeGoal
from nd_robotic.robot.goal.kind.suprise_poise.suprise_poise import SuprisePoise
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.trace.group.group import Group as TraceGroup
from nd_robotic.robot.structure.structure import Structure
from nd_utility.os.file_system.directory.directory import Directory


class Robot(ABC):
    """
    A robot is a singletone that is acceptable for comunication therough the structure
    """
    _instance = None

    def __new__(cls, structure:Structure, *args, **kwargs):
        """
        dont assign a name in args, a born baby doent know its name
        Args:
            structure:
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize(structure)
        return cls._instance

    def _initialize(self, structure):
        self._structure = structure

        self._composite_goal = None
        self._composite_action = None
        self.__name = None

        self.__run()

    @classmethod
    def init_from_directory(cls, os_directory: Directory):
        # TODO: To be completed
        structure = Structure()
        return cls(structure)

    def get_structure(self) -> Structure:
        return self._structure

    def set_name(self, name: str) -> None:
        """
        usually called in a population of robots
        a robot, on its birth doesnt name, but it should get the information as the structure
        Args:
            name:

        Returns:

        """
        self.__name = name

    def get_structure(self) -> Structure:
        return self._structure

    def get_name(self) -> Optional[str]:
        if self.__name is None:
            raise ValueError("name was never set. This robt is nameless. Call set_name() first")
        return self.__name

    def attach_goal(self, parent_goal: CompositeGoal, goal: ComponentGoal) -> None:
        """
        We can just attach goals and not actions. Planning in mind>process>thinking>decision making  makes a composite action
        Args:
            parent_goal:
            goal:

        Returns:

        """
        self._composite_goal.get_child(parent_goal).add_child(goal)

    def handle_request(self, trace_group: TraceGroup):
        ...

    def __run(self):
        from nd_robotic.robot.structure.kind.mind.cognition.process.kind.thinking.decision_making.planning.planning import \
            Planning

        # All goals must be attached to this one so that teh robot decides the priority between them
        suprise_poise_goal = SuprisePoise()

        self._composite_goal = CompositeGoal(suprise_poise_goal, None)
        planner = Planning(self._composite_goal)
        self._composite_action = planner.get_composite_action()

        self._composite_action.run()

    def get_memory_episodes(self):
        pass

    def get_priming_memory(self):
        pass
