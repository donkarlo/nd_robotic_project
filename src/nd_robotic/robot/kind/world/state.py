from nd_physics.quantity.tensor_quantifiable import TensorQuantifiable
from nd_robotic.robot.robot import StateChangeObserver


class State(TensorQuantifiable):
    def __init__(self):
        pass

    def attach_state_change_obersever(self, state_change_observer:StateChangeObserver)->None:
        """

        Args:
            state_change_observer: such as a robot etc

        Returns:

        """
        ...