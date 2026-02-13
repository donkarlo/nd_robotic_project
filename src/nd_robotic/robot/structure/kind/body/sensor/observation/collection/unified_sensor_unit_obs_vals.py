from typing import List
from nd_math.linear_algebra.vec.vec import Vec
from nd_physics.dimension.unit.unit import Unit


class UnifiedSensorUnitObsVals:
    def __init__(self, sensor:Sensor, val_unit: Unit, time_unit: Unit, vals:List[Vec] = None):
        self._sensor = sensor
        self._time_unit = time_unit
        self._val_unit = val_unit
        self._vals = vals

        # initial mission_state
        self._vals = []

    def add_val(self, val: Vec):
        self._val_list.append(val)
