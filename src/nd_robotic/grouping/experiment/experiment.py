from abc import ABC
from typing import List

from nd_robotic_group_project.experiment.scenario import Scenario


class Experiment:
    """
    We know in a robotic inner_experiment a robot tries to achieve a initial_mission
    """

    class Experiment(ABC):
        """
        We know in a robotic inner_experiment a robot tries to achieve a initial_mission
        """

        def __init__(self, learning_scenarios: List[Scenario], testing_scenarios: List[Scenario]) -> None:
            self._testing_scenarios = testing_scenarios
            self._learning_scenarios = learning_scenarios

        def get_learning_scenarios(self) -> List[Scenario]:
            return self._learning_scenarios

        def get_testing_scenarios(self) -> List[Scenario]:
            return self._testing_scenarios

        def run_learning_scenarios(self):
            for learning_scenario in self._learning_scenarios:
                learning_scenario.learn()

        def run_testing_scenarios(self):
            for testing_scenario in self._testing_scenarios:
                testing_scenario.run()