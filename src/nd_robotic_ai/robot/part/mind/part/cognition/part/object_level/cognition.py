from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.process import Process
from nd_robotic_ai.robot.composition.composite import Composite as RobotCompositeUnit

class Cognition(RobotCompositeUnit):
    """
    -  the processing parts of the mind
    - Bridge between language and ontology by decision making and acting
    - 
    """
    def __init__(self):
        RobotCompositeUnit.__init__(self)
        self.add_child(Process())