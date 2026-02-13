from nd_math.linear_algebra.tensor.tensor import Tensor
from typing import Union
import numpy as np

class State:
    """
    It should cover both mental and physical state
    """

    def __init__(self, value: np.ndarray):
        """
        Originally it is not a vector but it is verctor representable
        Args:
            value:
        """
        self._value = value

    def get_value(self) -> np.ndarray:
        return self._value
