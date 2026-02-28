from typing import Protocol, runtime_checkable

from nd_physics.quantity.quantifiable import Quantifiable


@runtime_checkable
class Interface(Quantifiable, Protocol): ...
