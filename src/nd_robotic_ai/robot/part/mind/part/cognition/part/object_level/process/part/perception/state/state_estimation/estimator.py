from sensorx.observation.sensor_set_obss import SensorSetObss


class Estimator:
    def __init__(self, sensor_set_obss:SensorSetObss):
        self._sensor_set_obss:SensorSetObss = sensor_set_obss

