from nd_physics.dimension.unit.scalar import Scalar
from nd_physics.dimension.unit.vec import Vec as UnitedVec
from nd_robotic.robot.robot import Observation


class Factory:
    @staticmethod
    def get_timed_obs(united_val: UnitedVec, united_time:Scalar)->Interface:
        return Timed(Observation(united_val, united_time))

