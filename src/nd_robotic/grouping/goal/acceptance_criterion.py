from abc import ABC, abstractmethod
from nd_robotic.mind.cognition.process.kind.perception.state.state import State


class AcceptanceCriterion(ABC):
    """
    Defines an abstract interface for checking whether a composite_goal has been achieved.
    Subclasses implement specific acceptance logic.
    """

    @abstractmethod
    def is_satisfied(self, current_state: State, desired_state: State) -> bool:
        pass
