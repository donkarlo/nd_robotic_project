from typing import List, Protocol, runtime_checkable

from nd_robotic_ai.mind.cognition.process.kind.memory.composite.observer.trace.creation_subscriber import TraceCreationSubscriber
from nd_robotic_ai.robot.composition.kind.mind.meta_cognition.cognition.process.composition.child.memory.composition.trace.trace import Trace

@runtime_checkable
class CreationPublisher(Protocol):
    """
    it seems that any memory component can be a creation subcriber
    """
    _trace_creation_subscribers: List[TraceCreationSubscriber]

    def attach_trace_creation_subscriber(self, subscriber: TraceCreationSubscriber) -> None: ...

    def detach_trace_creation_subscriber(self, subscriber: TraceCreationSubscriber) -> None: ...

    def notify_trace_creation_subscribers(self, trace: Trace) -> None: ...