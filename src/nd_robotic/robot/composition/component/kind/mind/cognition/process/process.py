"""
https://en.wikipedia.org/wiki/Category:Mental_processes
"""
from abc import ABC, abstractmethod

from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.attention.attention import Attention
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.learning.learning import Learning
from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.thinking.thiniking import Thinking


class Process(ABC):
    def __init__(self, memory, perception, attention:Attention, thinking:Thinking, learning:Learning):
        pass