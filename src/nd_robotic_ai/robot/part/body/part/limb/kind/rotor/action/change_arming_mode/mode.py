from dataclasses import dataclass
from enum import IntEnum, auto


class Mode(IntEnum):
    DISARMED = auto()
    ARMED = auto()