"""
https://en.wikipedia.org/wiki/Category:Mental_processes
"""
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.attention.attention import \
    Attention
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.learning.learning import Learning
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.memory import Memory
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.perception.perception import \
    Perception
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.thinking.thiniking import \
    Thinking
from nd_robotic_ai.robot.composition.composite import Composite as RobotCompositeComponent


class Process(RobotCompositeComponent):
    def __init__(self):
        """
        memory, percepting, attention: Attention, thinking: Thinking, learning: Learning
        """
        RobotCompositeComponent.__init__(self)
        self.add_children([Memory(), Learning(), Thinking(), Perception(), Attention()])