from typing import Protocol, runtime_checkable

from nd_robotic.robot.composition.component.kind.mind.cognition.process.kind.memory.composite.trace.trace import Trace

@runtime_checkable
class TraceCreationSubscriber(Protocol):
    def do_with_created_trace(self, trace: Trace)->None: ...