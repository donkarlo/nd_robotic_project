from nd_robotic.robot.robot import Interface


class Message(Interface):
    """Message is a action_potential_group strcture such as a directed graph or oop_based objects or a tree graph that can be contributed to
    describe an entity to an agent for descison making in now or future.
    - How to build:
        - from action_potential polulation sequence firings
        - from corpus
        - first from action_potential population sequences to corpus and then to episodic
        - episodic is what ever that describes an entity, mind or body. This description might cause generation of a action or a new description or discarded
    """
    def __init__(self):
        """
            can be a directed Graph or a tree Graph or an object in OOP
        """
        pass

    def init_from_spike_populations_sequence(self, spike_populations_sequence:SpikesPopulationSequence):
        pass

    def init_from_language(self):
        """Such as describing a tree action_potential_group structure"""
        pass

    def init_from_spike_populations_squence_to_language_to_message(self):
        """Such as describing a tree action_potential_group structure"""
        pass