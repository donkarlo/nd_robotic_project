from nd_robotic.mind.cognition.process.kind.memory.kind.long_term.implicit.conditioned.conditioned import Conditioned
from nd_robotic.mind.cognition.process.kind.memory.kind.long_term.implicit.habitual.habitual import Habitual
from nd_robotic.mind.cognition.process.kind.memory.kind.long_term.implicit.priming.priming import Priming
from nd_robotic.mind.cognition.process.kind.memory.kind.long_term.implicit.procedural.procedural import Procedural


class Implicit:
    """
    - associated with a lack of conscious event_specific_knowledge/awareness of the previously experienced information.
    - skills:
        _ After a skill is learned_parameters, performance of that skill reflects nonconscious memory. For example, after a person learns to ride a bike, they don’t think about rotating the pedals, steering, braking, or balancing. Instead, their conscious event_specific_knowledge is dominated by where they want to ride or whatever else they happen to be thinking about.
    """
    def __init__(self):
        """
        loading by order that human brain loads
        """
        self._procedural = Procedural()
        self._priming = Priming()
        self._conditioned = Conditioned()
        self._habitual = Habitual()