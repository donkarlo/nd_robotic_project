from abc import ABC, abstractmethod
import numpy as np

class Interface(ABC):
    @abstractmethod
    def __init__(self, value: np.ndarray):
        pass

    @abstractmethod
    def get_value(self):
        pass
