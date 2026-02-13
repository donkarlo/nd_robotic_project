from nd_robotic.robot.robot import Sensor


class Lidar(Sensor):
    def __init__(self, ranges_dim:int):
        self._ranges_dim = ranges_dim
