from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.composite import \
    Composite as CompositeMemory
from nd_math.probability.statistic.population.sampling.kind.countable.finite.members_mentioned.numbered.sequence.sliding_window.sliding_window import \
    SlidingWindow
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.action.kind.intra.segregating.segregating import Segregating
import numpy as np
from typing import Tuple

class AutoCorrelating(Segregating):
    """
    To break a periodicity sequence into its periods
    """
    def __init__(self, composite_memory:CompositeMemory):
        ...



    def _build_segregated_components(self, sliding_window:SlidingWindow)->Tuple[np.ndarray, np.ndarray]:
        ...