from abc import ABC, abstractmethod

from nd_math.probability.distribution.discrepancy.discrepancy import Discrepancy
from nd_robotic.robot.state.state import State


class Acceptance(ABC):
    """
    Defines an abstract interface for checking whether a composite_goal has been achieved.
    Subclasses implement specific acceptance logic.
    """

    def __init__(self, discrepancy_method: Discrepancy, threshold: float):
        """

        Args:
            prior: such as prior in Bayesian
            descripency_class: such as Kullback-Leibler divergence
            threshold: Can be achieved by tarining with normal scenario and then test it with normal scenario and then abverage ±
        """
        self._threshold = threshold
        self._discrepancy_method = discrepancy_method


    def is_satisfied(self, desired_state:State, current_state:State) -> bool:
        if self._discrepancy_method.get_discrepancy_value(desired_state, current_state) < self._threshold:
            return True
        else:
            return False


    def get_acceptance_rate(self, desired_state: State, current_state: State) -> float:
        """
        This can be a probabilty distribution based on:
            - train-test data
        Args:
            desired_state:
            current_state:

        Returns:

        """
        return self._discrepancy_method.get_discrepancy_value(desired_state, current_state)
