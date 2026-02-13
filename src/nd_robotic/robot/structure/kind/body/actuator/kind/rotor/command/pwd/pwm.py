from nd_robotic.robot.robot import Command
from nd_physics.dimension.unit.scalar import Scalar


class Pwm(Command):
    """
    Pulse Width Modulation TODO: maybe this has somthing to do with neural action_potentials
    """
    def __init__(self, time:Scalar=0):
        """

        Args:
            time: is usually in microseconds
        """
        self._time = time
        super().__init__()

    def get_time(self):
        return self._time