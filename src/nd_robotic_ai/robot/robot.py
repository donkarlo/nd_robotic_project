from nd_robotic_ai.robot.composition.composite import Composite as RobotComposite
from nd_robotic_ai.robot.part.body.body import Body
from nd_robotic_ai.robot.part.body.part.nervous_system.part.neuron.kind.sensory.part.receptor.receptor import \
    Receptor
from nd_robotic_ai.robot.part.mind.mind import Mind
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.perception.perception import \
    Perception
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.thinking.part.planning.planning import \
    Planning
from nd_robotic_ai.robot.part.mind.state.kind.dead.dead import Dead
from nd_robotic_ai.robot.part.mind.state.kind.idle.mind_wandering import MindWandering
from nd_robotic_ai.robot.part.stimulus.observer.kind.mind_state_change.mind_state_change import MindStateChange


class Robot(RobotComposite):
    """
    A robot is a singletone that is acceptable for comunication therough the structure
    Each robot is an intersection between mind and body, it relates a Train of ActionPotential Train (NeuralCoding) to a trace_formation society formatted data
    """

    def __init__(self):
        """
        dont assign a title in args, a born baby doent know its title
        Args:
            structure:
        """
        RobotComposite.__init__(self)

        self.add_child(Body())
        self.add_child(Mind())

    def enliven(self) -> None:
        # All goals must be attached to this one so that teh robot decides the priority between them
        stimulus = MindStateChange(Dead(), MindWandering())

        mind_state_receptor = self.find_component_by_name(Receptor)

        mind_state_receptor.receive_stimulus(stimulus)

        perception = self.find_component_by_name(Perception)

        perception.notify_trace_formation_subscribers()

        planning = self.find_component_by_name(Planning)
        planning.run()
