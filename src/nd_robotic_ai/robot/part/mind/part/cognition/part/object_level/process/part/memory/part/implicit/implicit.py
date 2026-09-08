from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.implicit.repetition_priming.repetition_priming import \
    RepetitionPriming
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.part.implicit.skill.skill import \
    Skill
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.composite import Composite as MemoryComposite

class Implicit(MemoryComposite):
    """
    - associated with a lack of conscious event_specific_knowledge_forcasting_model_config/awareness of the previously experienced information.
    - skills:
        _ After a skill is learned_parameters, performance of that skill reflects nonconscious memory. For example, after a person learns to ride a bike, they don’t think about rotating the pedals, steering, braking, or balancing. Instead, their conscious event_specific_knowledge_forcasting_model_config is dominated by where they want to ride or whatever else they happen to be thinking about.
    """
    def __init__(self):
        """
        loading by order that human brain loads
        """
        MemoryComposite.__init__(self)
        self.add_child(RepetitionPriming())
        self.add_child(Skill())