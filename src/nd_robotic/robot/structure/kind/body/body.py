from nd_robotic.robot.robot import Collection as ActuatorCollection
from nd_robotic.robot.robot import Group as SensorCollection

class Body:
    def __init__(self, actuator_collection: ActuatorCollection, sensors_collection: SensorCollection):
        self._actuators:ActuatorCollection = actuator_collection
        self._sensor_collection = sensors_collection

    def get_actuators(self)->ActuatorCollection:
        return self._actuators

    def get_sensors(self)->SensorCollection:
        return self._sensor_collection

    def sensor_addition_observer(self):
        """
        When a new sensor is added probably things like this might happen
        - individual segragted predictive models such as when an IMU is added, then GPS Predicting models nad LIDAR Predicting models can be probably improved?
        """
        pass

    def actuator_addition_observer(self):
        pass



