from nd_robotic_ai.robot.composition.composite import Composite as RobotCompositeComponent


class Attention(RobotCompositeComponent):
    """
    if you consider a humen, an attention can be absobed to a parts of a time_based serie by a watch alarm
    """
    def __init__(self):
        RobotCompositeComponent.__init__(self)