from nd_robotic.experiment.scenario import Scenario
from typing import List
from abc import ABC


class Experiment(ABC):
    """
    We know in a robotic experiment a robot tries to achieve a initial_mission
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
