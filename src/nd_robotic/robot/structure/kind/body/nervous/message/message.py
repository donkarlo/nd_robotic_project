from nd_physics.dimension.unit.unit import Unit
from nd_robotic.body.nerve.neuron import Neuron
from nd_robotic.body.nerve.spike.spike import Spike
from nd_robotic.robot.robot import Sensor


class Message:
    """
    - TODO: I have decide to replace Message with trace
    - a message must have a generator os_file and a channel and a destination
    - many of these messages make one trace in mind>memory>episodic>episod>trace
    - This message is not a ROS message, ROS message already a role of trace so it is
    """
    def __init__(self, spike, gneration_time:Time, channel, source:Union[Sensor, Mind], destination:Union[Mind, actuator]):
        self._generation_time = gneration_time
        self._spike = spike
        self._channel = channel

    def get_rate(self, unit:Unit)->float:
        """calculate base on frequency of nueurons_spikes_times"""
        pass

    def get_existing_label_or_create_new_label(self)->Morephem:
        pass