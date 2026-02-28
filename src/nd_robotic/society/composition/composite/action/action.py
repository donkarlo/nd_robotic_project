from abc import ABC, abstractmethod
from nd_robotic.robot.goal.goal import Goal

class Action(ABC):
    """
    Acording to ROS2: Actions are one of the communicating types in ROS 2 and are
    intended for long running missions. They consist of three parts: a role, feedback, and a result.
    - GoalGain is assessable
    - It is also an abstraction. what we call a verb in NLP
    - MAVLINK defines actions
    - if an role is breakable to smaller actions then it is actually a GoalGain
    - History will be kept in episodes
    """
    def __init__(self, goal:Goal):
        self._goal = goal

    def get_goal(self)->Goal:
        return self._goal

    @abstractmethod
    def run(self):
        pass