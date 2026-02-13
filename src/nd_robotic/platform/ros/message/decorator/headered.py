from nd_robotic.platform.ros.message.kind.header.header import Header
from nd_robotic.platform.ros.message.interface import Interface


class Headered(Decorator):
    def __init__(self, inner:Interface, header:Header):
        super().__init__(inner)
        self._header = header

    def get_header(self) -> Header:
        return self._header