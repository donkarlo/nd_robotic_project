from abc import ABC
from typing import Optional


from nd_robotic.robot.composition.component.kind.body.body import Body
from nd_robotic.robot.composition.component.kind.mind.mind import Mind
from nd_robotic.robot.composition.composite import Composite as RobotCompositUnit
from nd_robotic.robot.goal.composite.component import Component as ComponentGoal
from nd_robotic.robot.goal.composite.composite import Composite as CompositeGoal
from nd_robotic.robot.goal.kind.suprise_poise.suprise_poise import SurprisePoise
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.trace.group.group import Group as TraceGroup
from nd_robotic.robot.composition.structure.structure import Structure
from nd_utility.os.file_system.directory.directory import Directory
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.thinking.decision_making.planning.planning import \
    Planning



class Robot(RobotCompositUnit, ABC):
    """
    A robot is a singletone that is acceptable for comunication therough the structure
    Each robot is an intersection between mind and body, it relates a Group of ActionPotential Group (NeuralCoding) to a trace group formatted data
    """

    def __init__(self):
        """
        dont assign a title in args, a born baby doent know its title
        Args:
            structure:
        """
        RobotCompositUnit.__init__(self)

        self._composite_goal = None
        self._composite_action = None

        self.add_child(Body())
        self.add_child(Mind())



    @classmethod
    def init_from_directory(cls, os_directory: Directory):
        # TODO: To be completed
        return cls(os_directory)

    def set_name(self, name: str) -> None:
        """
        usually called in a population of robots
        a robot, on its birth doesnt title, but it should get the information as the structure
        Args:
            name:

        Returns:

        """
        self.__name = name

    def get_structure(self) -> Structure:
        return self._structure

    def get_name(self) -> Optional[str]:
        if self.__name is None:
            raise ValueError("title was never set. This robt is nameless. Call set_name() first")
        return self.__name

    def attach_goal(self, parent_goal: CompositeGoal, goal: ComponentGoal) -> None:
        """
        We can just attach goals and not actions. Planning in mind>process>thinking>decision making  makes a composition action
        Args:
            parent_goal:
            goal:

        Returns:

        """
        self._composite_goal.get_child(parent_goal).add_child(goal)

    def handle_request(self, trace_group: TraceGroup):
        ...

    def run(self):


        # All goals must be attached to this one so that teh robot decides the priority between them
        suprise_poise_goal = SurprisePoise()

        self._composite_goal = CompositeGoal(suprise_poise_goal, None)
        planner = Planning(self._composite_goal)
        self._composite_action = planner.get_composite_action()

        self._composite_action.run()

    def get_memory_episodes(self):
        pass

    def get_priming_memory(self):
        pass
