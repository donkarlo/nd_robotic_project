
from nd_math.probability.statistic.population.sampling.kind.countable.finite.members_mentioned.numbered.sequence.sliding_window.sliding_window import \
    SlidingWindow

import numpy as np
from typing import Tuple

from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.action.kind.intra.segregating.segregating import \
    Segregating
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.composite import \
    Composite as MemoryComposite


class AutoCorrelating(Segregating):
    """
    To break a periodicity sequence into its periods
    """
    def __init__(self, composite_memory: MemoryComposite):
        ...



    def _build_segregated_components(self, sliding_window:SlidingWindow)->Tuple[np.ndarray, np.ndarray]:
        ...