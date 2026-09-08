from abc import abstractmethod, ABC
from typing import List

class Level(ABC):
    @abstractmethod
    def run_tests(self)->List[float]:
        pass