from typing import Protocol, List


class Interface(Protocol):
    def get_on_reception_uncertainty_reduction_rate(self, recievers:List) -> float: ...