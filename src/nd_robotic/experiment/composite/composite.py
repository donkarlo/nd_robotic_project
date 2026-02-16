from typing import Optional

from nd_robotic.experiment.composite.component import Component
from nd_robotic.experiment.experiment import Experiment
from nd_utility.oop.design_pattern.structural.composite.composite import Composite as BaseComposite


class Composite(Component, BaseComposite):
    """
    Composite node that can hold other Components.
    """

    def __init__(self, inner_experiment: Experiment, name: Optional[str]):
        BaseComposite.__init__(self, inner_experiment, name)
        Component.__init__(self, name)
