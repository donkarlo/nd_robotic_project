from nd_robotic_ai.robot.composition.composite import Composite as RobotComposite
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.leaf.leaf import \
    Group
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.leaf.leaf import \
    Trace


class Episode(RobotComposite):
    def __init__(self):
        """
        composed of time, location, event(particular occurrences of actions and their properties)
        """
        RobotComposite.__init__(self)
