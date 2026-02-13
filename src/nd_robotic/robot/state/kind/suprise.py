from nd_math.probability.distribution.distribution import Distribution
from nd_robotic.robot.state.state import State


class Suprise(State):
    """

    """
    def __init__(self, value:float):
        # this is kullback libler divergence and it is always a scalar
        State.__init__(self, value)