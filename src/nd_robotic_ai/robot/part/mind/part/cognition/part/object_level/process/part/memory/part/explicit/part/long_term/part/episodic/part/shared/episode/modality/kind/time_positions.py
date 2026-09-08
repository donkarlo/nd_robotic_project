

from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.long_term.part.episodic.part.shared.episode.modality.modality import Modality
from nd_utility.data.kind.dic.dic import Dic


class TimePositions(Modality):
    """
    DO not inject numpyz storage into this, how we store the data is different than how we remeber it
    """
    def __init__(self, dic:Dic):
        Modality.__init__(self, dic)

