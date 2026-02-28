from abc import ABC, abstractmethod

from nd_utility.oop.design_pattern.structural.composition.component import Component as BaseComponent


class Component(BaseComponent, ABC):
    """
    """

    def __init__(self):
        BaseComponent.__init__(self)

    @abstractmethod
    def run(self):
        pass
