from dataclasses import dataclass
from enum import IntEnum, auto


class Status(IntEnum):
    CW = auto()
    CCW = auto()