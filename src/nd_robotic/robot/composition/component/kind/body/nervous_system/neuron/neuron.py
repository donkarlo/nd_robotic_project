from nd_robotic.robot.composition.composite import Composite as RobotCompositeUnit
from nd_robotic.society.composition.composite.action.kind.communicating.neuron.spike import Spike


class Neuron(RobotCompositeUnit):
    def fire_spike(self, spike:Spike):
        pass