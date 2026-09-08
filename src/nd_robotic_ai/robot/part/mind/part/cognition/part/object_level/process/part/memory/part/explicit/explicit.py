from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.composite import Composite as MemoryComposite
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.long_term.long_term import \
    LongTerm

class Explicit(MemoryComposite):
    """
    This class is exactly the same as Component
    """

    def __init__(self):
        MemoryComposite.__init__(self)
        self.add_child(LongTerm())