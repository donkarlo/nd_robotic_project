sefrom nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.memory.composition.composite import \
    Composite as MemoryComposite
from nd_robotic_ai.robot.part.action.action import \
    Action as ActionComposite
from nd_robotic_ai.robot.part.goal.goal import \
    Goal as GoalComposite
from nd_robotic_ai.robot.part.goal.plan.plan import \
    Plan


class Semantic(MemoryComposite):
    """Semantic memory refers to general_events environment knowledge that humans have accumulated throughout their lives.
    -  Semantic information is derived from accumulated episodic memory. Episodic memory can be thought of as a "map" that ties together items in semantic memory. For example, all encounters with how a "dog" looks and sounds will make up the semantic representation of that word. All episodic memories concerning a dog will then reference this single semantic representation of "dog" and, likewise, all new experiences with the dog will modify the single semantic representation of that dog.
    - In semantic memory time_based doesnt exist
    - it is not personal unlike episodic memory
    - it is about knowledge and concept and events(as in episodic)
    """
    def __init__(self):
        MemoryComposite.__init__(self)
        self.add_child(GoalComposite())
        self.add_child(ActionComposite())
        self.add_child(Plan())