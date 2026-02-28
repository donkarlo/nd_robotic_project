from enum import Enum, auto


class Kind(Enum):
    """
    GoalGain kinds
    """
    SINGLE_SENSOR_SEQUENCE = auto()
    