from typing import Protocol, runtime_checkable

@runtime_checkable
class Segregatorable(Protocol):
    def segregate(self) -> None:
        pass