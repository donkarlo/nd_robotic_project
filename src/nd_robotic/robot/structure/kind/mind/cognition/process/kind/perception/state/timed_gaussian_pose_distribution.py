from nd_math.probability.distribution.parametricity.kind.parametric.covariance_matrix import CovarianceMatrix
from nd_math.probability.distribution.gaussian.distribution import Distribution
from nd_physics.dimension.unit.scalar import Scalar
from nd_physics.kinematics.pose import Pose


class TimedGaussianPoseDistribution(Distribution):
    def __init__(self, time:Scalar , mu:Pose, cov:CovarianceMatrix):
        super().__init__(mu, cov)
        self._time = time