from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.composite import Composite as MemoryComposite


class Composite(MemoryComposite):
    def __init__(self):
        """

        Args:
            internal_trace_group: can be None to only host the link (classification) to the next inner_experiment (trace_formation action_potential_group here) or classification (only link/classification or a trace_formation action_potential_group)
            name:
        """
        MemoryComposite.__init__(self)