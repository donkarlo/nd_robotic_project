from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.composite import \
    Composite as MemoryComposite
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.explicit.part.long_term.part.episodic.part.autobiographic.part.event_specific_knowledge.event_specific_knowledge import \
    EventSpecificKnowledge


class Autobiographic(MemoryComposite):
    """
    Whatever self is involved
    """

    def __init__(self):
        MemoryComposite.__init__(self)
        self.add_child(EventSpecificKnowledge())
