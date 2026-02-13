from nd_math.numbers.kind.real.interval.interval import Interval
from nd_robotic.robot.robot import Decorator


class Periodic(Decorator):
    def __init__(self, time_interval:Interval):
        self._time_interval = time_interval

    def get_time_interval(self):
        return self._time_interval