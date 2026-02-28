from nd_robotic.robot.robot import Messageable
from nd_math.probability.distribution.gaussian.distribution import Distribution


class GaussianPoseDestribution(Distribution, Messageable):
    def __init__(self, pose:Pose):
        pass