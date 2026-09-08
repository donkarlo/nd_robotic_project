from dataclasses import dataclass
from enum import IntEnum, auto


class Mode(IntEnum):
    COLOCK_WISE = auto()
    COUNTER_CLOCK_WISE = auto()