from abc import ABC, abstractmethod

from nd_robotic_ai.robot.part.action.action import Action
from nd_robotic_ai.robot.part.action.feedback.feedback import Feedback
from nd_robotic_ai.robot.part.goal.goal import Goal



class Controlling(Action, ABC):
    def __init__(self, action_to_run:Action, goal:Goal, actuator):
        self._action_to_run = action_to_run
        self._goal = goal

    @abstractmethod
    def run(self)->Feedback:
        pass

