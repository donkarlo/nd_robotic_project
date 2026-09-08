from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.long_term.part.episodic.part.shared.episode.episode import \
    Episode
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.long_term.part.episodic.part.shared.episode.modality.modality import \
    Modality
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.leaf.leaf import \
    Group
from nd_utility.data.kind.dic.dic import Dic


class MultiModal(Episode):
    def __init__(self, dic:Dic):
        """
        composed of time, location, event(particular occurrences of actions and their properties)
        """
        self._trace_group = Group()

    def add_modality(self, modality: Modality) -> None:
        self.add_child(modality)
