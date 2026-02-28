from nd_robotic.robot.composition.component.kind.body.nervous_system.neuron.neural_coding.action_potential.action_potential import ActionPotential


class NeuralCoding:
    """
    https://en.wikipedia.org/wiki/Neural_coding#Sparse_coding
    refers to the relationship between a stimulus and its respective neuronal responses, and the signalling relationships among networks of neurons in an ensemble.
    """
    def __init__(self, action_potentials:list[ActionPotential]):
        self._action_potentials = action_potentials

    def send_traces_to_structure_nodes_and_to_response_time_and_population__neurons_interval_and_voltage_assign_a_body_node(self):
        pass

    def get_aproximate_envoked_time(self):
        pass
    
    def get_approximate_somatotopic_locations(self):
        pass