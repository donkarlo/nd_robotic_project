from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.composite import Composite as MemoryComposite
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.trace.group.decorator.storaged import \
    Storaged
from nd_robotic.robot.structure.kind.mind.cognition.process.kind.memory.composite.trace.group.group import Group as StoragedTraceGroup
from nd_utility.oop.design_pattern.structural.decorator.decorator import Decorator


class  Episode(MemoryComposite):
    """
    Maybe different from Force, I should think about it
    - from what an episodic must be composed
        − GoalGain
        − pre_plan
        - mind world is formed by experoceptive
    """
    def __init__(self, tarce_group: StoragedTraceGroup):
        """

        Args:
            tarce_group: we need a action_potential_group of traces so large to get the information what-where-when-who
                - usually mixed_modelities.yaml is loaded into this class
        """
        if not Decorator.has_decorator(Storaged):
            raise TypeError("The Trace Group must have a storage for eposode. So build Storaged(StoragedTraceGroup)")
        MemoryComposite.__init__(self, tarce_group)
