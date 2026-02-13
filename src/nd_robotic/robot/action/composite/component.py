from abc import ABC, abstractmethod
from typing import Optional

from nd_utility.oop.design_pattern.structural.composite.component import Component as BaseComponent


class Component(BaseComponent, ABC):
    """
    """

    def __init__(self, name: Optional[str]):
        BaseComponent.__init__(self, name)

    @abstractmethod
    def run(self):
        pass
