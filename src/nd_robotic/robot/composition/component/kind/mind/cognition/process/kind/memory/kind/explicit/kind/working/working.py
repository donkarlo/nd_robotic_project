from nd_robotic.mind.cognition.process.kind.memory.composite.composite import Composite as MemoryTree
from nd_robotic.mind.cognition.process.kind.memory.composite.observer.trace.creation_subscriber import \
    TraceCreationSubscriber as TraceCreationSubcriber
from nd_robotic.mind.cognition.process.kind.memory.memorizing.memorizing import Memorizing
from nd_robotic.mind.cognition.process.kind.memory.remembering.remembering import Remembering
from nd_robotic.mind.cognition.process.kind.memory.kind.long_term.explicit.episodic.experience.group.group import Group as ExperienceGroup


class Working(TraceCreationSubcriber):
    """
    To represent working memory or short memory
    """

    def __init__(self):
        """
        Here we design the aritecture or philosophy of the memory. The body part is in body
        coupling memorizing, remebering and storing
        Args:
            memory_tree: contains short and long term memory tree
            memorizing: contains the strategy for memorizing something
            remembering: contains the strategy to remeber somethings

        """
        self._running_data = None

    def load_running_data(self)->None:
        pass

    def save(self)->None:
        pass

    def get_running_data(self):
        pass




