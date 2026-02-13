from nd_physics.dimension.unit.scalar import Scalar
from nd_physics.dimension.unit.unit import Unit
from abc import ABC, abstractmethod
from nd_math.linear_algebra.tensor.vector.vector import Vector


class Sensor(ABC):
    def __init__(self, type: str, unit:Unit, freq: Scalar):
        """
        Observation is decoupled from sensor. sensor holds observer dimension and average frequency and the unit in which the observer is is read
        Args:
            type: kind.schema.yaml is ncessary because we might have two identical GPS sensors
            unit: observer value unit unit
            freq:
        """
        self._type = type
        self._freq = freq
        self._unit = unit



    @abstractmethod
    def validate_observation(self, obs:Vector)->bool:
        pass

    def propogate