from typing import Optional, List

from nd_robotic_ai.robot.composition.composite import Composite as RobotCompositeComponent
from nd_robotic_ai.robot.part.action.action import Action
from nd_robotic_ai.robot.part.body.part.nervous_system.neural_coding.action_potential.action_potential import \
    ActionPotential
from nd_robotic_ai.robot.part.body.part.nervous_system.neural_coding.action_potential.observer.subscriber import \
    Subscriber as ActionPotentialSubcriber
from nd_robotic_ai.robot.part.mind.part.cognition.part.object_level.process.part.perception.trace.trace import \
    Trace
from nd_robotic_ai.robot.part.stimulus.observer.kind.mind_state_change.publisher import \
    Publisher as MindStateChangePublisher
from nd_robotic_ai.robot.part.stimulus.observer.kind.mind_state_change.subscriber import \
    Subscriber as MindStateChangeSubscriber
from nd_robotic_ai.robot.part.stimulus.observer.kind.trace_formation.publisher import \
    Publisher as TraceFormationPublisher
from nd_robotic_ai.robot.part.stimulus.observer.kind.trace_formation.subscriber import \
    Subscriber as TraceFormationSubscriber
from nd_utility.oop.design_pattern.architectural.pipes_and_filters.pipes_and_filters import PipesAndFilters
from nd_utility.oop.design_pattern.structural.composition.composite import Composite as BaseComposite
from nd_utility.oop.inheritance.overriding import override_from


class Perception(RobotCompositeComponent, ActionPotentialSubcriber, MindStateChangePublisher, TraceFormationPublisher,
                 Action):
    """
    - Perception is an action itself, so it consumes energy to make the agent aproach its goal
    Should I add the current observation point to a meaningful group and create an abstract concept, or should I pass it as it is planning?
    - Perception cqn be conscious and unconcious
    """

    def __init__(self):
        RobotCompositeComponent.__init__(self)

        self._action_potential_composite = BaseComposite()
        self._pipes_and_filters = PipesAndFilters()

        self._trace_formation_subscribers: List[TraceFormationSubscriber] = []

        self._mind_state_change_subscribers: List[MindStateChangeSubscriber] = []

    @override_from(ActionPotentialSubcriber, False, False)
    def handle_action_potential(self, action_potential: ActionPotential) -> Optional[Trace]:
        self._sort_action_potentials(action_potential)

    @override_from(TraceFormationPublisher, False, False)
    def attach_trace_formation_subscriber(self, trace_formation_subscriber: TraceFormationSubscriber) -> None:
        self._trace_formation_subscribers.append(trace_formation_subscriber)

    @override_from(TraceFormationPublisher, False, False)
    def notify_trace_formation_subscribers(self, formed_trace: Trace) -> None:
        for subscriber in self._trace_formation_subscribers:
            subscriber.notify_trace_formation(formed_trace)

    @override_from(MindStateChangePublisher, False, False)
    def notify_mind_state_change_subscribers(self, mind_state_change_subscriber: MindStateChangeSubscriber) -> None:
        for subscriber in self._mind_state_change_subscribers:
            subscriber.notify_mind_state_change(mind_state_change_subscriber)



    @override_from(Action, False, False)
    def run(self) -> None:
        pass
