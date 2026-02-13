from nd_robotic.mind.cognition.process.kind.memory.kind.long_term.modality.modality import Modality


class Cyclic:
    def __init__(self, modality:Modality, data:Any):
        """Data for one cycle of a modality in an event_specific_knowledge"""
        self._modality = modality
        #action_potential_group for a single cycle
        self._data = data

    def get_modality(self)->Modality:
        return self._modality