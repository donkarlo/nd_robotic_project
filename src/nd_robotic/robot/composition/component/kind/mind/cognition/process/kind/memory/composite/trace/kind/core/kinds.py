from enum import IntEnum, auto


class Group(IntEnum):
    """
    This is the dictionary of what can be placed in memory
    """
    pre_plan = auto()
    plan = auto()
    action = auto()
    command = auto()
    sensor_ob = auto()
    gaussianed_quaternion_kinematic = auto()
    lidar_scan_ranges = auto()
    human_command_remeber_experience = auto()
    seq2seq = auto()
