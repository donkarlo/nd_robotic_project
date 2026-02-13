from typing import Protocol, runtime_checkable

from nd_robotic.robot.robot import Group as SensorCollection
from nd_robotic.robot.robot import Collection as ObservationCollection


@runtime_checkable
class StateChangeObserver(Protocol):
    _sensor_collection: SensorCollection
    def get_observations(self, sensor_collection: SensorCollection)-> ObservationCollection:
        """

        Args:
            sensor_collection: all members must be of deocrator Sensored(Observation) so that we know to what sensor it belongs

        Returns:

        """
        ...