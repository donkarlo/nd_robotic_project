from typing import Protocol, runtime_checkable


@runtime_checkable
class Communicator(Protocol):
    def emmit_morpheme(self):
        pass
