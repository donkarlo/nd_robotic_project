from enum import IntEnum, auto


class Awareness(IntEnum):
    I_HAVE_ACTUATORS = auto()
    I_HAVE_SENSORS = auto()
    I_CAN_REMEMBER_EACH_SENSOR_MODALITY_INDEPENDENTLY = auto()
    pass