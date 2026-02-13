from nd_math.probability.distribution.kind.gaussian.gaussian import Gaussian
from nd_robotic.robot.state.decorator.decorator import Decorator
from nd_robotic.robot.state.interface import Interface as StateInterface


class Decoration(Decorator):
    def __init__(self, inner: StateInterface, guassian_distribution: Gaussian):
        Decorator.__init__(self, inner)
        self._guassian_distribution = guassian_distribution

    def get_gaussian_distribution(self) -> Gaussian:
        return self._guassian_distribution
