from dataclasses import dataclass
from enum import IntEnum, auto


class Status(IntEnum):
    DISARMED = auto()
    ARMED = auto()