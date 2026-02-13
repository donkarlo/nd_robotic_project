from typing import Protocol, runtime_checkable


class Communicatorable(Protocol):
    """An actuator that can create messages that carry traces"""
    def release_treable_message(self, channel):
        pass