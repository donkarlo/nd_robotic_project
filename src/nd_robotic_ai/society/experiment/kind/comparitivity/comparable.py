from nd_robotic_ai.experiment.experiment import Experiment


class Comparable(Experiment):
    """
    We know in a robotic inner_experiment a robot tries to achieve a initial_mission
    """

    def __init__(self, condition_one, condition_two) -> None:
        self._condition_one = condition_one
        self._condition_two = condition_two
