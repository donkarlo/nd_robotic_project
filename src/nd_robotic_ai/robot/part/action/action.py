from abc import abstractmethod, ABC

from nd_robotic_ai.robot.part.action.composition.composite import \
    Composite as ActionComposite
from nd_robotic_ai.robot.state.state import State


class Action(ActionComposite, ABC):
    """
    - Action is whatever consumes energy
    - This class represents available actions, not running actions
    - Action is whatever consumes resorces such as energy or health(for example spare classification)
    This action can become so granular that to a action to change voltage in a rotor so in ROS we replaced Action for both Plan and COmmand and mission
    examples of actions the subclasses should support:
    - body
        - Goto

    - Mind
        - memory segregating
        - Memory
            - memorize
            - remember
    """

    def __init__(self):
        ActionComposite.__init__(self)

    @abstractmethod
    def run(self) -> State:
        """
        This run will be propegated to top or mabe bottom actions
        Returns:

        """
        pass
