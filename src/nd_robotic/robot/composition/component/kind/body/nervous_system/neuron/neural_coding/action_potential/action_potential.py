from nd_physics.dimension.unit.unit import Unit

from nd_math.number.kind.real.interval.interval import Interval


class ActionPotential:
    """
    - It is also called Action Potential
    - https://en.wikipedia.org/wiki/Action_potential
    electrical load sent to brain or recived from brain. about 1ms and 100 milli volts
    - it is not curvy, it goes up suddenly and comes down suddenly
    - another __name is role potential or nerve impulse
    - action_potential is formed of power (Voltage) and duration (Duration)
    """

    def __init__(self, united_time_interval: Interval, time_unit: Unit, voltage_interval: Interval, voltage_unit: Unit):
        self._united_time_interval = united_time_interval
        self.action_potential = united_voltage_interval
