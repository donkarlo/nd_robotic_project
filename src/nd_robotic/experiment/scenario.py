from typing import Optional

from abc import ABC

from nd_robotic.robot.robot import Composite
from nd_robotic.robot.robot import Goal
from nd_robotic.robot.robot import Robot
from nd_physics.world.world import World


class Scenario(ABC):
    """
    Scenario is more than a robot and its missions
    """
    def __init__(self, robot:Robot, initial_mission:Goal, initial_plan: Composite, world:World, name:Optional[str]=None):
        """
        
        Args:
            robot: 
            initial_mission: 
            initial_plan: 
            world: 
            name:
        """
        self._robot = robot
        self._initial_mission = initial_mission
        self._initial_plan = initial_plan

        self._world = world
        self._name = name

        # run

    def run(self)->None:
        self._robot.achieve_mission(self._initial_mission)

    def learn(self):
        self._robot.learn()

    def get_world(self)->World:
        return self._world

    def get_mission(self)->Goal:
        return self._initial_mission

    def get_robot(self)->Robot:
        return self._robot

    def get_plan(self)->Composite:
        return self._initial_plan

    def get_name(self)->Optional[str]:
        return self._name