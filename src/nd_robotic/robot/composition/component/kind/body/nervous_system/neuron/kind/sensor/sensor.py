from nd_physics.dimension.unit.scalar import Scalar
from nd_physics.dimension.unit.unit import Unit
from abc import ABC
from nd_robotic.robot.composition.unit import Unit as RobotUnit


class Sensor(RobotUnit, ABC):
    def __init__(self, unit:Unit, freq: Scalar):
        """
        Observation is decoupled from sensor. sensor holds observer dimension and average frequency and the unit in which the observer is is read
        Args:
            type: composition.schema.yaml is ncessary because we might have two identical GPS sensors
            unit: observer value unit unit
            freq:
        """
        self._type = type
        self._freq = freq
        self._unit = unit
