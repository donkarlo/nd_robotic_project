from nd_physics.kinematics.pose import Pose


class Odometry:
    def __init__(self, motion_sensor_set_vals: SensorSetVals):
        self._sensor_set_vals:SensorSetVals = motion_sensor_set_vals

    def get_pose(self)->Pose:
        pass