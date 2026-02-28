from nd_robotic.robot.composition.component.kind.mind.cognition.process.process import Process
from nd_robotic.robot.composition.composite import Composite as RobotCompositeComponent

class Cognition(RobotCompositeComponent):
    """
    -  the processing part of the mind
    - Bridge between language and ontology by decision making and acting
    - 
    """
    def __init__(self, process:Process):
        RobotCompositeComponent.__init__(self)