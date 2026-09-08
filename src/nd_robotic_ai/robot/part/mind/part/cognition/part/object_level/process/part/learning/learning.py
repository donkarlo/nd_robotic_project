from typing import List
from nd_robotic_ai.robot.composition.composite import Composite as RobotCompositeComponent

class Learning(RobotCompositeComponent):
    """
    - learning is the matter of updating a models parameter according to new eveidences(Observation)
    """
    def __init__(self):
        RobotCompositeComponent.__init__(self)

    def update_model_parameters(self, model_parameters:List) -> None:
        pass

    def learn(self):
        pass
